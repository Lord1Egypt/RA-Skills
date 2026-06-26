#!/usr/bin/env python3
"""
DeepSpeed Training Launcher for Fine-tuning LLMs
Supports LoRA, QLoRA, full fine-tuning with ZeRO optimization
"""

import os
import sys
import json
import torch
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    HfArgumentParser,
    set_seed,
    DataCollatorForSeq2Seq,
)
from datasets import load_dataset, Dataset
import deepspeed

# Early Stopping
from transformers import EarlyStoppingCallback

# PEFT imports (optional)
try:
    from peft import (
        LoraConfig,
        get_peft_model,
        prepare_model_for_kbit_training,
        TaskType,
        PeftModel,
    )
    PEFT_AVAILABLE = True
except ImportError:
    PEFT_AVAILABLE = False
    logging.warning("PEFT not installed. LoRA/QLoRA features will be unavailable.")

# BitsAndBytes for 4-bit quantization (optional)
try:
    from transformers import BitsAndBytesConfig
    BNB_AVAILABLE = True
except ImportError:
    BNB_AVAILABLE = False


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@dataclass
class ModelArguments:
    """Arguments pertaining to which model/config/tokenizer we are going to fine-tune."""
    
    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    trust_remote_code: bool = field(
        default=False,
        metadata={"help": "Whether to trust remote code when loading model"}
    )
    torch_dtype: str = field(
        default="auto",
        metadata={"help": "Torch dtype: auto, bfloat16, float16, float32"}
    )
    use_flash_attention: bool = field(
        default=False,
        metadata={"help": "Use Flash Attention 2 if available"}
    )


@dataclass
class DataArguments:
    """Arguments pertaining to what data we are going to input our model for training."""
    
    dataset_path: str = field(
        metadata={"help": "Path to the training dataset (local dir or HuggingFace dataset)"}
    )
    dataset_config: Optional[str] = field(
        default=None,
        metadata={"help": "Dataset configuration name"}
    )
    text_column: str = field(
        default="text",
        metadata={"help": "Column name containing the text data"}
    )
    instruction_column: Optional[str] = field(
        default=None,
        metadata={"help": "Column name for instruction (for instruction tuning)"}
    )
    output_column: Optional[str] = field(
        default=None,
        metadata={"help": "Column name for expected output (for instruction tuning)"}
    )
    max_seq_length: int = field(
        default=2048,
        metadata={"help": "Maximum sequence length"}
    )
    packing: bool = field(
        default=False,
        metadata={"help": "Use packing for more efficient training"}
    )


@dataclass
class PeftArguments:
    """Arguments for PEFT/LoRA training."""
    
    use_peft: bool = field(
        default=False,
        metadata={"help": "Use PEFT (LoRA) for training"}
    )
    peft_method: str = field(
        default="lora",
        metadata={"help": "PEFT method: lora, qlora, etc."}
    )
    lora_r: int = field(
        default=16,
        metadata={"help": "LoRA attention dimension"}
    )
    lora_alpha: int = field(
        default=32,
        metadata={"help": "LoRA alpha parameter"}
    )
    lora_dropout: float = field(
        default=0.05,
        metadata={"help": "LoRA dropout"}
    )
    lora_target_modules: Optional[str] = field(
        default=None,
        metadata={"help": "Comma-separated target modules (default: q_proj,v_proj,k_proj,o_proj)"}
    )
    use_rslora: bool = field(
        default=False,
        metadata={"help": "Use Rank-Stabilized LoRA"}
    )
    # 4-bit quantization for QLoRA
    load_in_4bit: bool = field(
        default=False,
        metadata={"help": "Load model in 4-bit (for QLoRA)"}
    )
    bnb_4bit_quant_type: str = field(
        default="nf4",
        metadata={"help": "4-bit quantization type: fp4 or nf4"}
    )
    bnb_4bit_compute_dtype: str = field(
        default="bfloat16",
        metadata={"help": "Compute dtype for 4-bit base model"}
    )
    use_nested_quant: bool = field(
        default=True,
        metadata={"help": "Use nested quantization for 4-bit"}
    )


@dataclass
class EarlyStoppingArguments:
    """Arguments for early stopping."""
    
    early_stopping_patience: int = field(
        default=0,
        metadata={"help": "Early stopping patience (number of evals with no improvement). 0 = disabled."}
    )
    early_stopping_threshold: float = field(
        default=0.0,
        metadata={"help": "Minimum change in eval loss to qualify as improvement. Default 0.0 = any decrease counts."}
    )


def load_model_and_tokenizer(
    model_args: ModelArguments,
    peft_args: PeftArguments,
):
    """Load model and tokenizer with appropriate config."""
    
    logger.info(f"Loading model: {model_args.model_name_or_path}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_args.model_name_or_path,
        trust_remote_code=model_args.trust_remote_code,
        padding_side="right",
    )
    
    # Set pad token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Determine torch dtype
    if model_args.torch_dtype == "auto":
        torch_dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16
    else:
        torch_dtype = getattr(torch, model_args.torch_dtype)
    
    # Prepare quantization config for QLoRA
    quantization_config = None
    if peft_args.load_in_4bit and BNB_AVAILABLE:
        logger.info("Loading model in 4-bit for QLoRA")
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type=peft_args.bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=getattr(torch, peft_args.bnb_4bit_compute_dtype),
            bnb_4bit_use_double_quant=peft_args.use_nested_quant,
        )
    
    # Load model
    model_kwargs = {
        "torch_dtype": torch_dtype,
        "trust_remote_code": model_args.trust_remote_code,
    }
    
    if quantization_config:
        model_kwargs["quantization_config"] = quantization_config
    
    if model_args.use_flash_attention:
        model_kwargs["attn_implementation"] = "flash_attention_2"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_args.model_name_or_path,
        **model_kwargs
    )
    
    # Prepare model for k-bit training if using QLoRA
    if peft_args.load_in_4bit and PEFT_AVAILABLE:
        model = prepare_model_for_kbit_training(model)
    
    return model, tokenizer


def setup_peft_model(model, peft_args: PeftArguments):
    """Setup PEFT/LoRA adapters on the model."""
    
    if not peft_args.use_peft or not PEFT_AVAILABLE:
        return model
    
    logger.info(f"Setting up {peft_args.peft_method.upper()} with r={peft_args.lora_r}, alpha={peft_args.lora_alpha}")
    
    # Determine target modules
    if peft_args.lora_target_modules:
        target_modules = peft_args.lora_target_modules.split(",")
    else:
        # Default target modules for most LLMs
        target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]
    
    peft_config = LoraConfig(
        r=peft_args.lora_r,
        lora_alpha=peft_args.lora_alpha,
        target_modules=target_modules,
        lora_dropout=peft_args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        use_rslora=peft_args.use_rslora,
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    return model


def prepare_dataset(data_args: DataArguments, tokenizer):
    """Load and prepare the dataset for training."""
    
    logger.info(f"Loading dataset from: {data_args.dataset_path}")
    
    # Load dataset
    if Path(data_args.dataset_path).exists():
        # Local dataset
        if Path(data_args.dataset_path).is_dir():
            dataset = load_dataset(
                data_args.dataset_path,
                data_files={"train": "train.*", "validation": "val.*", "test": "test.*"}
            )
        else:
            dataset = load_dataset(Path(data_args.dataset_path).suffix[1:], data_files=data_args.dataset_path)
    else:
        # HuggingFace dataset
        dataset = load_dataset(
            data_args.dataset_path,
            data_args.dataset_config,
            split="train"
        )
    
    # Tokenization function
    def tokenize_function(examples):
        if data_args.instruction_column and data_args.output_column:
            # Instruction tuning format
            prompts = [
                f"{instr}\n{inp}"
                for instr, inp in zip(examples[data_args.instruction_column], examples.get(data_args.text_column, [""]*len(examples)))
            ]
            responses = examples[data_args.output_column]
            
            texts = [f"{p}\n{r}" for p, r in zip(prompts, responses)]
        else:
            # Simple text continuation
            texts = examples[data_args.text_column]
        
        # Tokenize
        result = tokenizer(
            texts,
            truncation=True,
            max_length=data_args.max_seq_length,
            padding=False,
            return_tensors=None,
        )
        
        # Add labels (same as input_ids for causal LM)
        result["labels"] = result["input_ids"].copy()
        
        return result
    
    # Apply tokenization
    if isinstance(dataset, dict):
        tokenized_datasets = {k: v.map(tokenize_function, batched=True, remove_columns=v.column_names) for k, v in dataset.items()}
        train_dataset = tokenized_datasets.get("train")
        eval_dataset = tokenized_datasets.get("validation")
    else:
        train_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
        eval_dataset = None
    
    return train_dataset, eval_dataset


def main():
    """Main training entry point."""
    
    parser = HfArgumentParser((ModelArguments, DataArguments, PeftArguments, EarlyStoppingArguments, TrainingArguments))
    
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # Parse from JSON config
        model_args, data_args, peft_args, es_args, training_args = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        # Parse from command line
        model_args, data_args, peft_args, es_args, training_args = parser.parse_args_into_dataclasses()
    
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO if training_args.local_rank in [-1, 0] else logging.WARN,
    )
    
    # Set seed
    set_seed(training_args.seed)
    
    # Log arguments
    logger.info(f"Model args: {model_args}")
    logger.info(f"Data args: {data_args}")
    logger.info(f"PEFT args: {peft_args}")
    logger.info(f"Early Stopping args: {es_args}")
    logger.info(f"Training args: {training_args}")
    
    # Configure early stopping
    callbacks = []
    if es_args.early_stopping_patience > 0:
        # Early stopping requires eval to be enabled and best model tracking
        if not training_args.eval_strategy:
            logger.warning("Early stopping enabled but eval_strategy is not set. Setting eval_strategy='steps' with eval_steps=500.")
            training_args.eval_strategy = "steps"
            training_args.eval_steps = 500
        if not training_args.load_best_model_at_end:
            logger.info("Enabling load_best_model_at_end for early stopping.")
            training_args.load_best_model_at_end = True
            training_args.metric_for_best_model = "eval_loss"
            training_args.greater_is_better = False
            # Ensure save_strategy matches eval_strategy for best model tracking
            if training_args.save_strategy != training_args.eval_strategy:
                logger.info(f"Setting save_strategy to match eval_strategy: {training_args.eval_strategy}")
                training_args.save_strategy = training_args.eval_strategy
                training_args.save_steps = training_args.eval_steps
        
        callbacks.append(EarlyStoppingCallback(
            early_stopping_patience=es_args.early_stopping_patience,
            early_stopping_threshold=es_args.early_stopping_threshold,
        ))
        logger.info(f"Early stopping enabled: patience={es_args.early_stopping_patience}, threshold={es_args.early_stopping_threshold}")
    
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(model_args, peft_args)
    
    # Setup PEFT if enabled
    model = setup_peft_model(model, peft_args)
    
    # Prepare dataset
    train_dataset, eval_dataset = prepare_dataset(data_args, tokenizer)
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, pad_to_multiple_of=8),
        callbacks=callbacks if callbacks else None,
    )
    
    # Training
    logger.info("*** Starting training ***")
    train_result = trainer.train(resume_from_checkpoint=training_args.resume_from_checkpoint)
    
    metrics = train_result.metrics
    trainer.save_model()
    
    if trainer.is_world_process_zero():
        # Save metrics
        import json
        with open(os.path.join(training_args.output_dir, "train_results.json"), "w") as f:
            json.dump(metrics, f, indent=2)
        
        # Save training arguments
        torch.save(training_args, os.path.join(training_args.output_dir, "training_args.bin"))
    
    # Evaluation
    if training_args.do_eval and eval_dataset is not None:
        logger.info("*** Evaluate ***")
        metrics = trainer.evaluate()
        
        if trainer.is_world_process_zero():
            with open(os.path.join(training_args.output_dir, "eval_results.json"), "w") as f:
                json.dump(metrics, f, indent=2)
    
    logger.info("*** Training complete ***")


if __name__ == "__main__":
    main()
