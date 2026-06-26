#!/usr/bin/env python3
"""
DeepSpeed Configuration Generator
Generates ZeRO configuration files for different optimization stages.
"""

import json
import argparse
from typing import Dict, Any, Optional


def generate_zero_config(
    zero_stage: int = 2,
    offload_optimizer: bool = False,
    offload_param: bool = False,
    offload_device: str = "cpu",
    nvme_path: Optional[str] = None,
    overlap_comm: bool = True,
    contiguous_gradients: bool = True,
    sub_group_size: int = 1e9,
    reduce_bucket_size: str = "auto",
    stage3_prefetch_bucket_size: str = "auto",
    stage3_param_persistence_threshold: str = "auto",
    stage3_max_live_parameters: int = 1e9,
    stage3_max_reuse_distance: int = 1e9,
    bf16_enabled: bool = True,
    fp16_enabled: bool = False,
    gradient_accumulation_steps: str = "auto",
    gradient_clipping: str = "auto",
    train_batch_size: str = "auto",
    train_micro_batch_size_per_gpu: str = "auto",
    wall_clock_breakdown: bool = False,
) -> Dict[str, Any]:
    """
    Generate a DeepSpeed ZeRO configuration.
    
    Args:
        zero_stage: ZeRO optimization stage (0, 1, 2, 3)
        offload_optimizer: Offload optimizer states to CPU/NVMe
        offload_param: Offload parameters to CPU/NVMe (ZeRO-3 only)
        offload_device: Device for offloading ("cpu", "nvme", "none")
        nvme_path: Path to NVMe device for offloading
        overlap_comm: Overlap communication with computation
        contiguous_gradients: Use contiguous memory for gradients
        bf16_enabled: Enable bfloat16 mixed precision
        fp16_enabled: Enable float16 mixed precision
        
    Returns:
        DeepSpeed configuration dictionary
    """
    
    config = {
        "bf16": {
            "enabled": bf16_enabled
        },
        "fp16": {
            "enabled": fp16_enabled
        },
        "zero_optimization": {
            "stage": zero_stage,
            "overlap_comm": overlap_comm,
            "contiguous_gradients": contiguous_gradients,
            "sub_group_size": sub_group_size,
            "reduce_bucket_size": reduce_bucket_size,
        },
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "gradient_clipping": gradient_clipping,
        "train_batch_size": train_batch_size,
        "train_micro_batch_size_per_gpu": train_micro_batch_size_per_gpu,
        "wall_clock_breakdown": wall_clock_breakdown,
    }
    
    # ZeRO-3 specific settings
    if zero_stage == 3:
        config["zero_optimization"].update({
            "stage3_prefetch_bucket_size": stage3_prefetch_bucket_size,
            "stage3_param_persistence_threshold": stage3_param_persistence_threshold,
            "stage3_max_live_parameters": stage3_max_live_parameters,
            "stage3_max_reuse_distance": stage3_max_reuse_distance,
            "gather_16bit_weights_on_model_save": True,
        })
    
    # Optimizer offloading
    if offload_optimizer and zero_stage >= 2:
        offload_config = {
            "device": offload_device,
            "pin_memory": True if offload_device == "cpu" else False,
        }
        
        if offload_device == "nvme" and nvme_path:
            offload_config["nvme_path"] = nvme_path
        
        config["zero_optimization"]["offload_optimizer"] = offload_config
    
    # Parameter offloading (ZeRO-3 only)
    if offload_param and zero_stage == 3:
        offload_config = {
            "device": offload_device,
            "pin_memory": True if offload_device == "cpu" else False,
        }
        
        if offload_device == "nvme" and nvme_path:
            offload_config["nvme_path"] = nvme_path
        
        config["zero_optimization"]["offload_param"] = offload_config
    
    return config


def main():
    parser = argparse.ArgumentParser(description="Generate DeepSpeed ZeRO configuration")
    
    parser.add_argument("--zero-stage", type=int, default=2, choices=[0, 1, 2, 3],
                        help="ZeRO optimization stage")
    parser.add_argument("--offload-optimizer", action="store_true",
                        help="Offload optimizer states")
    parser.add_argument("--offload-param", action="store_true",
                        help="Offload parameters (ZeRO-3 only)")
    parser.add_argument("--offload-device", type=str, default="cpu", choices=["cpu", "nvme", "none"],
                        help="Device for offloading")
    parser.add_argument("--nvme-path", type=str, default=None,
                        help="Path to NVMe device for offloading")
    parser.add_argument("--bf16", action="store_true", default=True,
                        help="Enable bfloat16")
    parser.add_argument("--fp16", action="store_true",
                        help="Enable float16")
    parser.add_argument("--output", type=str, default="ds_config.json",
                        help="Output config file path")
    
    args = parser.parse_args()
    
    # Generate config
    config = generate_zero_config(
        zero_stage=args.zero_stage,
        offload_optimizer=args.offload_optimizer,
        offload_param=args.offload_param,
        offload_device=args.offload_device,
        nvme_path=args.nvme_path,
        bf16_enabled=args.bf16,
        fp16_enabled=args.fp16,
    )
    
    # Save config
    with open(args.output, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"DeepSpeed config saved to: {args.output}")
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()
