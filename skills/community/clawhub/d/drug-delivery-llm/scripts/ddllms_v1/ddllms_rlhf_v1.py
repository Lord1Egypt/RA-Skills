import json
from dataclasses import dataclass
from typing import Optional, Tuple
import torch
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset
from trl import CPOConfig, CPOTrainer, ORPOConfig, ORPOTrainer, BCOConfig, BCOTrainer
from transformers import (
    Gemma2ForCausalLM,
    GPTNeoXForCausalLM,
    OlmoeForCausalLM,
    Qwen3MoeForCausalLM,
    DeepseekV3ForCausalLM,
    GraniteMoeForCausalLM,
    GemmaForCausalLM,
)
def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)
@dataclass
class CausalLMOutputWithAuxLoss(ModelOutput):
    logits: torch.FloatTensor
    loss: Optional[torch.FloatTensor] = None
    past_key_values: Optional[Tuple[Tuple[torch.FloatTensor]]] = None
    hidden_states: Optional[Tuple[torch.FloatTensor]] = None
    attentions: Optional[Tuple[torch.FloatTensor]] = None
    aux_loss: Optional[torch.FloatTensor] = None
class MultiModelWrapper(PreTrainedModel):
    MODEL_CLASSES = {
        "gemma2": Gemma2ForCausalLM,
        "gptneox": GPTNeoXForCausalLM,
        "olmoe": OlmoeForCausalLM,
        "qwen3": Qwen3MoeForCausalLM,
        "dpv3": DeepseekV3ForCausalLM,
        "granite": GraniteMoeForCausalLM,
        "gpt2": GPT2LMHeadModel,
        "gemma": GemmaForCausalLM,
    }
    def __init__(self, model_type: str, model_dir: str):
        assert model_type in self.MODEL_CLASSES, f"Unsupported model_type: {model_type}"
        super().__init__(self.MODEL_CLASSES[model_type].from_pretrained(model_dir).config)
        self.base_model = self.MODEL_CLASSES[model_type].from_pretrained(model_dir, output_attentions=True)
        self.config = self.base_model.config
    def forward(self, *args, **kwargs) -> CausalLMOutputWithAuxLoss:
        output = self.base_model(*args, **kwargs)
        return CausalLMOutputWithAuxLoss(
            logits=output.logits,
            loss=getattr(output, "loss", None),
            past_key_values=getattr(output, "past_key_values", None),
            hidden_states=getattr(output, "hidden_states", None),
            attentions=getattr(output, "attentions", None),
            aux_loss=torch.tensor(0.0, device=output.logits.device),
        )
# -------- 配置 --------
def run(
    model_type: str,
    model_dir: str,
    tokenizer_path: str,
    data_path: str,
    output_dir: str,
    trainer_type: str = "cpo",  # options: "cpo", "orpo", "bco"
    lora_r: int = 12,
    lora_alpha: int = 32,
    lora_dropout: float = 0.2,
    batch_size: int = 256,
    max_epochs: int = 200,
    max_length: int = 64,
    learning_rate: float = 5e-4,
    seed: int = 42,
):
    data_dict = load_json_file(data_path)
    dataset = Dataset.from_dict(data_dict)
    tokenizer = SMILESBPETokenizer.get_hf_tokenizer(tokenizer_path, model_max_length=max_length)
    model = MultiModelWrapper(model_type=model_type, model_dir=model_dir)
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
    )
    model = get_peft_model(model, peft_config)
    trainer_map = {
        "cpo": (CPOConfig, CPOTrainer),
        "orpo": (ORPOConfig, ORPOTrainer),
        "bco": (BCOConfig, BCOTrainer),
    }
    assert trainer_type in trainer_map, f"Unsupported trainer_type: {trainer_type}"
    ConfigClass, TrainerClass = trainer_map[trainer_type]
    training_args = ConfigClass(
        output_dir=output_dir,
        logging_steps=10,
        per_device_train_batch_size=batch_size,
        max_epochs=max_epochs,
        learning_rate=learning_rate,
        seed=seed,
    )
    trainer = TrainerClass(
        model=model,
        args=training_args,
        processing_class=tokenizer,
        train_dataset=dataset,
    )
    trainer.train()
    # 存
    model.base_model.save_pretrained(f"{output_dir}/{model_type}")
    print(f"Training with {trainer_type.upper()} complete. Model saved at {output_dir}/{model_type}")
# -------- 按需运行并调整参数 --------
if __name__ == "__main__":
    run(
        model_type="gptneox",
        model_dir="YOUR_PATH/model-base",
        tokenizer_path="YOUR_PATH/tokenizer.json",
        data_path="YOUR_RLDATA.json",
        output_dir="neox-cpo",
        trainer_type="cpo",
        batch_size=256,
        max_epochs=80,
        learning_rate=5e-4,
)