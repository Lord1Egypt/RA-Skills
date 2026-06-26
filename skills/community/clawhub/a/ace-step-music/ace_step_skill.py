#!/usr/bin/env python3
"""
ACE-Step 1.5 Music Generation Skill for OpenClaw
封装 ACE-Step，提供简单易用的 Agent 调用接口
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# 配置
DEFAULT_MODEL_PATH = os.path.expanduser("~/workspace/ace-step/models")
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Music/ACE-Step")
VENV_PATH = os.path.expanduser("~/ace-step-env")

class ACEStepSkill:
    """ACE-Step 1.5 音乐生成 Skill"""
    
    def __init__(self, model_path: str = None, device: str = "mps"):
        self.model_path = model_path or DEFAULT_MODEL_PATH
        self.device = device
        self.backend = "mlx"  # Apple Silicon 最优
        self._check_installation()
    
    def _check_installation(self) -> bool:
        """检查 ACE-Step 是否已安装"""
        venv_python = os.path.join(VENV_PATH, "bin", "python")
        if not os.path.exists(venv_python):
            raise RuntimeError(
                f"ACE-Step 环境未找到: {VENV_PATH}\n"
                "请先运行安装: ./install_ace_step.sh"
            )
        return True
    
    def _run_in_venv(self, cmd: list) -> subprocess.CompletedProcess:
        """在虚拟环境中运行命令"""
        venv_python = os.path.join(VENV_PATH, "bin", "python")
        full_cmd = [venv_python] + cmd
        return subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            cwd=os.path.expanduser("~/workspace/ace-step")
        )
    
    def generate(
        self,
        prompt: str,
        duration: int = 30,
        temperature: float = 0.8,
        output_path: str = None,
        style: str = None
    ) -> Dict[str, Any]:
        """
        生成音乐
        
        Args:
            prompt: 音乐描述文本
            duration: 时长(秒)，默认30
            temperature: 创意程度 0-1，默认0.8
            output_path: 输出文件路径
            style: 风格标签
        
        Returns:
            包含 file_path, duration, generation_time 的字典
        """
        start_time = time.time()
        
        # 准备输出路径
        if output_path is None:
            os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
            timestamp = int(time.time())
            output_path = os.path.join(
                DEFAULT_OUTPUT_DIR, 
                f"ace_step_{timestamp}.wav"
            )
        
        # 构建生成脚本
        script = f'''
import sys
sys.path.insert(0, "{os.path.expanduser('~/workspace/ace-step')}")

from ace_step import MusicGenerator

generator = MusicGenerator(
    model_path="{self.model_path}",
    device="{self.device}",
    backend="{self.backend}"
)

music = generator.generate(
    prompt="{prompt}",
    duration={duration},
    temperature={temperature}
)

music.save("{output_path}")
print(f"SAVED: {{output_path}}")
'''
        
        # 执行生成
        result = self._run_in_venv(["-c", script])
        
        generation_time = time.time() - start_time
        
        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr,
                "generation_time": generation_time
            }
        
        return {
            "success": True,
            "file_path": output_path,
            "duration": duration,
            "generation_time": round(generation_time, 2),
            "prompt": prompt,
            "temperature": temperature
        }
    
    def check_system(self) -> Dict[str, Any]:
        """检查系统状态和性能"""
        import platform
        
        info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "device": self.device,
            "backend": self.backend,
            "model_path": self.model_path,
            "venv_exists": os.path.exists(VENV_PATH),
            "model_exists": os.path.exists(self.model_path)
        }
        
        # 检查 MLX
        try:
            result = self._run_in_venv(["-c", "import mlx; print(mlx.__version__)"])
            info["mlx_version"] = result.stdout.strip() if result.returncode == 0 else "not installed"
        except:
            info["mlx_version"] = "check failed"
        
        return info
    
    def batch_generate(
        self,
        prompts: list,
        duration: int = 30,
        output_dir: str = None
    ) -> list:
        """批量生成音乐"""
        if output_dir is None:
            output_dir = DEFAULT_OUTPUT_DIR
        
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for i, prompt in enumerate(prompts):
            output_path = os.path.join(output_dir, f"batch_{i:03d}.wav")
            result = self.generate(
                prompt=prompt,
                duration=duration,
                output_path=output_path
            )
            results.append(result)
        
        return results


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ACE-Step Music Generator")
    parser.add_argument("prompt", help="Music description")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--temperature", type=float, default=0.8, help="Creativity (0-1)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--check", action="store_true", help="Check system status")
    
    args = parser.parse_args()
    
    if args.check:
        skill = ACEStepSkill()
        info = skill.check_system()
        print(json.dumps(info, indent=2))
        return
    
    # 生成音乐
    skill = ACEStepSkill()
    result = skill.generate(
        prompt=args.prompt,
        duration=args.duration,
        temperature=args.temperature,
        output_path=args.output
    )
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
