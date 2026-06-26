---
name: f5tts_monitor
description: Monitor F5-TTS distributed training on the 9-GPU mining rig (Local-LLM) without interfering with the process.
metadata: {"clawdbot":{"emoji":"📦"}}
---

# F5-TTS Mining Rig Monitor Skill

This skill provides instructions for ADA to safely monitor the ongoing F5-TTS training process on the 9-GPU mining rig (`Local-LLM`), without interfering with the data or environment.

**IMPORTANT:** 
1. The training dataset and checkpoints are strictly located on the HDD of the mining rig at `/mnt/toshiba/projects/F5-TTS/`.
2. Do not attempt to run training locally on `asus-z170k`.
3. Use `uv` exclusively when interacting with the Python environment on the mining rig.

## Steps to Monitor Training

### 1. Check GPU Utilization
To ensure all 9 GPUs are actively training and not bottlenecked or OOMed, run the following command via SSH (remember to use pseudo-terminal if using watch):
```bash
ssh Local-LLM "nvidia-smi"
```
You should see 9 `python3` processes consistently consuming ~11GB of VRAM each.

### 2. Check Training Epoch Progress
Check the Accelerate training logs to see the current epoch and global step:
```bash
ssh Local-LLM "tail -n 100 /mnt/toshiba/projects/F5-TTS/outputs/training_mining_rig.log"
```
Look for `Epoch:` and `Step:` progression.

### 3. Check System RAM and CPU Load
The mining rig only has a 2-core Pentium CPU and 16GB of RAM. Make sure the system isn't buckling under the DDP overhead:
```bash
ssh Local-LLM "free -h && uptime"
```

### 4. Update the Heartbeat
After successfully probing the status, update your HEARTBEAT.md files locally to report the current Epoch, Step, GPU temperature, and estimated time remaining to Master Seiya.
