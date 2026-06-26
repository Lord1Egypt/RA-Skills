import argparse
from dd_tokenizer_base_v1 import SMILESBPETokenizer, LDataModule
from transformers import (
    GPT2Config, GPT2LMHeadModel,
    GPTNeoXConfig, GPTNeoXForCausalLM,
    GemmaConfig, GemmaForCausalLM,
    Gemma2Config, Gemma2ForCausalLM,
)
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
import llm
# === 配置===
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, required=True,
                        choices=["gpt2", "gptneox", "gemma", "gemma2"],
                        help="Type of Dense model to train")
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
    if model_type == "gpt2":
        config = GPT2Config(vocab_size=tokenizer.vocab_size,
                    bos_token_id=tokenizer.bos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    n_layer=hyperparams["n_layer"],
                    n_head=hyperparams["n_head"],
                    n_embd=hyperparams["n_embd"],
                    n_positions=hyperparams["max_length"],
                    n_ctx=hyperparams["max_length"])
        return GPT2LMHeadModel(config)
    elif model_type == "gpt2neox":
        config = GPTNeoXConfig(vocab_size = tokenizer.vocab_size,
                       hidden_size=256,
                       intermediate_size = 1024,
                       max_position_embeddings = 128,
                       num_hidden_layer = 12,
                       num_attention_heads = 16,
                       hidden_act = 'gelu',
                       rotary_pct = 0.25,
                       rotary_emb_base = 10000,
                       attention_dropout = 0.0,
                       hidden_dropout = 0.0,
                       initializer_range = 0.02,
                       layer_norm_eps = 1e-05,
                       use_cache = True,
                       bos_token_id = tokenizer.bos_token_id,
                       eos_token_id = tokenizer.eos_token_id,
                       tie_word_embeddings = False,
                       use_parallel_residual = True,
                       rope_scaling = None,
                       ttention_bias = True,
                       )
        return GPTNeoXForCausalLM(config)
    elif model_type == "gemma":
        config = GemmaConfig(vocab_size=tokenizer.vocab_size,
                     bos_token_id=tokenizer.bos_token_id,
                     eos_token_id=tokenizer.eos_token_id,
                     num_hidden_layer=hyperparams["n_layer"],
                     num_attention_heads=hyperparams["n_head"],
                     num_key_value_heads=hyperparams["n_head"],
                     head_dim=64,
                     hidden_size=1024,
                     intermediate_size = 8076,
                     max_position_embeddings=2730,
                     use_cache = True,
                     attention_bias = False,
                     attention_dropout = 0.0,
                     initializer_range = 0.02,
                     rms_norm_eps = 1e-05,
                     )
        return GemmaForCausalLM(config)
    elif model_type == "gemma2":
        config   =  Gemma2Config(vocab_size = tokenizer.vocab_size,
                         hidden_size= 1536,
                         intermediate_size = 4096,
                         max_position_embeddings = 64,
                         num_hidden_layer = 12, 
                         num_attention_heads = 8,
                         num_key_value_heads=4,
                         hidden_dim = 128,
                         max_position_embdding = 1024,
                         rms_norm_eps = 1e-05,
                         attention_dropout = 0.0,
                         initializer_range = 0.02,
                         use_cache = True,
                         cache_implementation = 'hybrid',
                         bos_token_id = tokenizer.bos_token_id,
                         eos_token_id = tokenizer.eos_token_id,
                         query_pre_attn_scalar = 128,
                         tie_word_embeddings = False,
                         rope_theta= 1000,
                         attention_bias = True,
                         sliding_window = 1024,
                         output_router_logits=True,
                        )
        return Gemma2ForCausalLM(config)
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