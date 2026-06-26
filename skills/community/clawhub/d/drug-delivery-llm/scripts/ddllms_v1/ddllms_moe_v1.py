import argparse
from dd_tokenizer_base_v1 import SMILESBPETokenizer, LDataModule
from transformers import (
    OlmoeConfig, OlmoeForCausalLM,
    Qwen3MoeConfig, Qwen3MoeForCausalLM,
    DeepseekV3Config, DeepseekV3ForCausalLM,
    GraniteMoeConfig, GraniteMoeForCausalLM,
)
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
import llm
# === 配置===
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, required=True,
                        choices=["olmoe", "qwen3moe", "deepseekv3", "granitemoe"],
                        help="Type of MoE model to train")
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--checkpoint_path", type=str, required=True)
    return parser.parse_args()
# === 超参===
hyperparams = {
    "batch_size": BNUM,
    "max_epochs": MAX_ENUM,
    "min_epochs" MIN_ENUM,
    "max_length": MAX_LNUM,
    "learning_rate": 5e-4,
    "final_learning_rate": 5e-8,
    "weight_decay": 0.0,
    "adam_eps": 1e-8,
    "adam_betas": (0.9, 0.999),
    "scheduler_T_max": 150_000,
    "vocab_size": 1076,
}
# ===MoE模型===
def build_model(model_type, tokenizer):
    if model_type == "olmoe":
        config = OlmoeConfig(
            vocab_size=tokenizer.vocab_size,
            hidden_size=192,
            intermediate_size=1024,
            max_position_embeddings=128,
            num_hidden_layer=12,
            num_attention_heads=16,
            hidden_act='gelu',
            attention_dropout=0.0,
            initializer_range=0.02,
            use_cache=True,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            tie_word_embeddings=False,
            rope_scaling=None,
            attention_bias=True,
            output_router_logits=True,
        )
        return OlmoeForCausalLM(config)
    elif model_type == "qwen3moe":
        config = Qwen3MoeConfig(
            vocab_size=tokenizer.vocab_size,
            hidden_size=96,
            intermediate_size=1024,
            max_position_embeddings=64,
            num_hidden_layer=12,
            num_attention_heads=16,
            hidden_act='silu',
            attention_dropout=0.0,
            initializer_range=0.02,
            use_cache=True,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            tie_word_embeddings=False,
            rope_scaling=None,
            attention_bias=True,
            output_router_logits=True,
        )
        return Qwen3MoeForCausalLM(config)
    elif model_type == "deepseekv3":
        config = DeepseekV3Config(
            vocab_size=tokenizer.vocab_size,
            hidden_size=72,
            intermediate_size=128,
            max_position_embeddings=32,
            moe_intermediate_size=256,
            n_shared_experts=1,
            n_routed_experts=128,
            num_hidden_layer=12,
            num_attention_heads=12,
            num_key_value_heads=12,
            hidden_act='silu',
            attention_dropout=0.0,
            initializer_range=0.02,
            use_cache=True,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            tie_word_embeddings=False,
            rope_scaling=None,
            attention_bias=True,
            output_router_logits=True,
        )
        return DeepseekV3ForCausalLM(config)
    elif model_type == "granitemoe":
        config = GraniteMoeConfig(
            vocab_size=tokenizer.vocab_size,
            hidden_size=256,
            intermediate_size=256,
            max_position_embeddings=32,
            moe_intermediate_size=256,
            num_local_experts=128,
            num_hidden_layer=12,
            num_attention_heads=16,
            num_key_value_heads=16,
            hidden_act='silu',
            attention_dropout=0.0,
            initializer_range=0.02,
            use_cache=True,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            tie_word_embeddings=False,
            rope_scaling=None,
            attention_bias=True,
            output_router_logits=True,
        )
        return GraniteMoeForCausalLM(config)
# === 运行===
def main():
    args = parse_args()
    # 预
    tokenizer = SMILESBPETokenizer.get_hf_tokenizer(
        'checkpoints/250k/tokenizer.json',
        model_max_length=hyperparams["max_length"]
    )
    # 数
    datamodule = LDataModule(
        args.data_path, tokenizer,
        batch_size=hyperparams["batch_size"],
        num_workers=4
    )
    #调
    model = build_model(args.model_type.lower(), tokenizer)
    checkpoint_cb = ModelCheckpoint(dirpath=f"{args.checkpoint_path}/model/", monitor="ppl_epoch", mode="min")
    early_stopping_cb = EarlyStopping(
        monitor="ppl_epoch",
        patience=2,
        min_delta=5e-3,
        check_finite=True,
        stopping_threshold=1.1,
        divergence_threshold=hyperparams["vocab_size"] / 10,
        verbose=True,
        mode="min",
        check_on_train_epoch_end=True,
    )
    # 配置
    trainer = Trainer(
        strategy="ddp",
        accelerator="gpu",
        devices=-1,
        callbacks=[checkpoint_cb, early_stopping_cb],
        max_epochs=hyperparams["max_epochs"],
        min_epochs=hyperparams["min_epochs"],
        val_check_interval=0.4,
        limit_train_batches=0.5,
        log_every_n_steps=200,
    )
    lit_model = LLMLitModel(
        model,
        batch_size=hyperparams["batch_size"],
        learning_rate=hyperparams["learning_rate"],
        final_learning_rate=hyperparams["final_learning_rate"],
        weight_decay=hyperparams["weight_decay"],
        adam_eps=hyperparams["adam_eps"],
        adam_betas=hyperparams["adam_betas"],
        scheduler_T_max=hyperparams["scheduler_T_max"],
    )
    # 训
    trainer.fit(lit_model, datamodule)
    # 参数保持
    lit_model.transformer.save_pretrained(f"{args.checkpoint_path}/model/")
if __name__ == "__main__":
    main()