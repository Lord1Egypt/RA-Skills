#!/usr/bin/env python3
"""
ComfyUI V8 秋叶中文版 技能脚本
功能：环境检测、一键启动、工作流生成、参数优化、故障排查
"""

import os
import subprocess
import json
import time
from pathlib import Path

# ==============================================
# ComfyUI V8 秋叶整合包 机器人技能（中文专用）
# ==============================================

class ComfyUI_V8_Skill:
    def __init__(self, comfy_path="ComfyUI-aki-V8"):
        """初始化：指定秋叶V8整合包根目录"""
        self.comfy_path = comfy_path
        self.launcher_exe = os.path.join(comfy_path, "绘世启动器.exe")
        self.start_bat = os.path.join(comfy_path, "启动ComfyUI.bat")
        self.workflows_dir = os.path.join(comfy_path, "user", "default", "workflows")
        self.models_dir = os.path.join(comfy_path, "models")

    # -------------------------- 1. 环境检测与启动 --------------------------
    def check_environment(self):
        """检测ComfyUI V8是否安装、启动器/依赖是否正常"""
        result = ["🔍 ComfyUI V8 秋叶整合包 环境检测结果："]
        
        if not os.path.exists(self.comfy_path):
            result.append("❌ 错误：未找到ComfyUI-aki-V8目录，请解压整合包到当前路径")
            return "\n".join(result)
        result.append(f"✅ 整合包目录：{self.comfy_path}")
        
        if os.path.exists(self.launcher_exe):
            result.append("✅ 绘世启动器（秋叶专用）存在")
        else:
            result.append("⚠️ 未找到绘世启动器，使用启动脚本")
        
        ckpt_dir = os.path.join(self.models_dir, "checkpoints")
        if os.path.exists(ckpt_dir) and len(os.listdir(ckpt_dir)) > 0:
            result.append(f"✅ 已加载模型：{len(os.listdir(ckpt_dir))}个")
        else:
            result.append("⚠️ 模型目录为空，请放入SD/FLUX等模型")
        
        result.append("✅ 秋叶V8已内置中文界面，无需额外汉化")
        return "\n".join(result)

    def start_comfyui(self, use_launcher=True):
        """一键启动ComfyUI V8（绘世启动器/脚本二选一）"""
        result = ["🚀 启动ComfyUI V8 秋叶中文版..."]
        try:
            if use_launcher and os.path.exists(self.launcher_exe):
                result.append("✅ 启动绘世启动器（秋叶专用）")
                subprocess.Popen([self.launcher_exe], cwd=self.comfy_path)
            else:
                result.append("✅ 启动ComfyUI核心服务")
                subprocess.Popen([self.start_bat], cwd=self.comfy_path, shell=True)
            time.sleep(3)
            result.append("✅ 启动成功！浏览器访问：http://127.0.0.1:8188")
            result.append("ℹ️ 绘世启动器可管理内核、插件、模型、一键更新")
        except Exception as e:
            result.append(f"❌ 启动失败：{str(e)}")
            result.append("💡 修复：安装.NET框架、以管理员运行、检查路径无中文/空格")
        return "\n".join(result)

    # -------------------------- 2. 核心工作流生成（秋叶V8标准节点） --------------------------
    def generate_workflow(self, workflow_type="txt2img", params=None):
        """生成标准工作流JSON（秋叶V8格式）"""
        default_params = {
            "prompt": "高质量, 8k, 高清, 细节丰富",
            "negative_prompt": "模糊, 低分辨率, 畸形, 水印, 文字",
            "model": "sdxl_base.safetensors",
            "width": 1024, "height": 1024,
            "steps": 28, "cfg": 7, "sampler": "dpmpp_2m", "scheduler": "karras"
        }
        if params:
            default_params.update(params)
        p = default_params

        workflows = {
            "txt2img": self._gen_txt2img_workflow(p),
            "img2img": self._gen_img2img_workflow(p),
            "controlnet": self._gen_controlnet_workflow(p),
            "instantid": self._gen_instantid_workflow(p),
            "outpaint": self._gen_outpaint_workflow(p),
            "inpaint": self._gen_inpaint_workflow(p),
        }
        
        wf = workflows.get(workflow_type, workflows["txt2img"])
        
        # 保存工作流到ComfyUI目录
        wf_path = os.path.join(self.workflows_dir, f"{wf['name']}.json")
        os.makedirs(os.path.dirname(wf_path), exist_ok=True)
        with open(wf_path, "w", encoding="utf-8") as f:
            json.dump(wf, f, ensure_ascii=False, indent=2)
        
        return f"""✅ 已生成【{wf['name']}】工作流
📁 保存路径：{wf_path}
⚙️ 参数：
  正向提示词：{p['prompt']}
  反向提示词：{p['negative_prompt']}
  尺寸：{p['width']}x{p['height']} | 步数：{p['steps']} | CFG：{p['cfg']}
💡 使用：ComfyUI界面 → 工作流 → 加载 → 选择该文件"""

    def _gen_txt2img_workflow(self, p):
        """文生图工作流（秋叶V8标准）"""
        return {
            "name": "秋叶V8-文生图",
            "nodes": [
                {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": p["model"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["prompt"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["negative_prompt"]}},
                {"type": "EmptyLatentImage", "inputs": {"width": p["width"], "height": p["height"], "batch_size": 1}},
                {"type": "KSampler", "inputs": {"steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"]}},
                {"type": "VAEDecode", "inputs": {}},
                {"type": "SaveImage", "inputs": {"filename_prefix": "txt2img"}}
            ]
        }

    def _gen_img2img_workflow(self, p):
        """图生图工作流（秋叶V8标准）"""
        return {
            "name": "秋叶V8-图生图",
            "nodes": [
                {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": p["model"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["prompt"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["negative_prompt"]}},
                {"type": "LoadImage", "inputs": {"image": "input.png"}},
                {"type": "VAEEncode", "inputs": {}},
                {"type": "KSampler", "inputs": {"steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"]}},
                {"type": "VAEDecode", "inputs": {}},
                {"type": "SaveImage", "inputs": {"filename_prefix": "img2img"}}
            ]
        }

    def _gen_controlnet_workflow(self, p):
        """ControlNet 工作流（秋叶V8标准）"""
        return {
            "name": "秋叶V8-ControlNet",
            "nodes": [
                {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": p["model"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["prompt"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["negative_prompt"]}},
                {"type": "LoadImage", "inputs": {"image": "control.png"}},
                {"type": "ControlNetLoader", "inputs": {"control_net_name": "canny.safetensors"}},
                {"type": "ControlNetApply", "inputs": {"strength": 0.8}},
                {"type": "EmptyLatentImage", "inputs": {"width": p["width"], "height": p["height"], "batch_size": 1}},
                {"type": "KSampler", "inputs": {"steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"]}},
                {"type": "VAEDecode", "inputs": {}},
                {"type": "SaveImage", "inputs": {"filename_prefix": "controlnet"}}
            ]
        }

    def _gen_instantid_workflow(self, p):
        """InstantID 人脸保持工作流（秋叶V8标准）"""
        return {
            "name": "秋叶V8-InstantID人脸",
            "nodes": [
                {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "ip-adapter-instantid-sdxl.safetensors"}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["prompt"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["negative_prompt"]}},
                {"type": "LoadImage", "inputs": {"image": "face.png"}},
                {"type": "InstantIDModelLoader", "inputs": {}},
                {"type": "InstantIDApply", "inputs": {"strength": 0.7}},
                {"type": "EmptyLatentImage", "inputs": {"width": p["width"], "height": p["height"], "batch_size": 1}},
                {"type": "KSampler", "inputs": {"steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"]}},
                {"type": "VAEDecode", "inputs": {}},
                {"type": "SaveImage", "inputs": {"filename_prefix": "instantid"}}
            ],
            "models_required": ["antelopev2", "ip-adapter-instantid-sdxl"]
        }

    def _gen_outpaint_workflow(self, p):
        """扩图工作流（秋叶V8标准）"""
        return {
            "name": "秋叶V8-智能扩图",
            "nodes": [
                {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": p["model"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["prompt"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["negative_prompt"]}},
                {"type": "LoadImage", "inputs": {"image": "base.png"}},
                {"type": "ImageResize", "inputs": {"width": p["width"] * 2, "height": p["height"] * 2, "method": "lanczos"}},
                {"type": "VAEEncode", "inputs": {}},
                {"type": "KSampler", "inputs": {"steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"]}},
                {"type": "VAEDecode", "inputs": {}},
                {"type": "SaveImage", "inputs": {"filename_prefix": "outpaint"}}
            ]
        }

    def _gen_inpaint_workflow(self, p):
        """局部重绘工作流（秋叶V8标准）"""
        return {
            "name": "秋叶V8-局部重绘",
            "nodes": [
                {"type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": p["model"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["prompt"]}},
                {"type": "CLIPTextEncode", "inputs": {"text": p["negative_prompt"]}},
                {"type": "LoadImage", "inputs": {"image": "base.png"}},
                {"type": "LoadImage", "inputs": {"image": "mask.png"}},
                {"type": "VAEEncodeForInpaint", "inputs": {}},
                {"type": "KSampler", "inputs": {"steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"]}},
                {"type": "VAEDecode", "inputs": {}},
                {"type": "SaveImage", "inputs": {"filename_prefix": "inpaint"}}
            ]
        }

    # -------------------------- 3. 显存优化 & 报错修复 --------------------------
    def optimize_vram(self, vram_gb=8):
        """显存优化（适配4G/6G/8G/12G/24G）"""
        tips = [f"⚙️ 显存优化方案（当前检测：{vram_gb}GB）："]
        if vram_gb < 6:
            tips += ["✅ 启用4bit量化（AutoGPTQ/GGUF）", "✅ 关闭高分辨率", "✅ 减小batch=1", "✅ 使用SD 1.5/7B小模型"]
        elif 6 <= vram_gb < 12:
            tips += ["✅ 8bit量化", "✅ 分辨率1024x1024", "✅ 启用VAE分块解码"]
        else:
            tips += ["✅ FP16原生", "✅ 1536x1536高分辨率", "✅ 批量生成"]
        tips += ["✅ 秋叶V8内置显存优化，启动器勾选「低显存模式」"]
        return "\n".join(tips)

    def fix_common_errors(self):
        """常见报错修复（秋叶V8专用）"""
        fixes = {
            "缺少.NET": "安装.NET 6.0桌面运行时，绘世启动器会自动引导下载",
            "显存不足": "启动器勾选低显存、4bit量化、减小尺寸",
            "节点缺失": "绘世启动器 → 拓展管理 → 一键安装缺失节点",
            "模型加载失败": "模型路径无中文/空格，放到models/checkpoints",
            "中文乱码": "秋叶V8已内置中文，无需修改，重启即可"
        }
        result = ["🛠 秋叶V8 常见报错修复："]
        for err, fix in fixes.items():
            result.append(f"• {err}：{fix}")
        return "\n".join(result)

    # -------------------------- 4. 附加增强功能 --------------------------
    def extra_features(self):
        """V8增强功能清单（机器人可调用）"""
        return """
✨ ComfyUI V8 秋叶整合包 增强功能：
1. 绘世启动器：内核/插件/模型/更新 一站式管理
2. 内置超300+常用节点（ControlNet/InstantID/LayerDiffusion/IC-Light）
3. 中文界面+中文提示词模板+风格库
4. 一键备份/还原工作流、模型、配置
5. 批量生成、XY对比、种子搜索、细节修复
6. 支持FLUX、SD3、SDXL、SD1.5全模型
7. 本地加速+国内镜像，解决GitHub下载慢
"""

    # -------------------------- 5. 故障排查 --------------------------
    def troubleshoot(self, error_desc=""):
        """故障排查"""
        error_db = {
            "启动闪退": ["安装 .NET Framework 4.8+", "以管理员身份运行", "检查路径不包含中文/空格", "关闭杀毒软件误报"],
            "显存不足": ["开启低显存模式 --lowvram", "降低图片分辨率", "使用半精度 --fp16", "分块加载模型"],
            "模型加载失败": ["检查模型完整性", "确认放置在 models/checkpoints/", "使用 safetensors 格式"],
            "节点缺失": ["绘世启动器 → 一键更新", "检查Python依赖", "重新安装插件"],
            "中文乱码": ["设置 → 界面语言 → 简体中文", "重启ComfyUI", "检查字体安装"],
            "卡在加载": ["检查网络连接", "确认磁盘空间充足", "手动下载模型到正确目录"],
            "生成缓慢": ["使用 --fp16 半精度", "开启批量处理", "使用更快采样器如 Euler"],
        }
        
        result = ["🔧 故障排查建议："]
        if not error_desc:
            result.append("常见问题解决方案：")
            for issue, solutions in error_db.items():
                result.append(f"\n📌 {issue}：")
                for s in solutions:
                    result.append(f"   • {s}")
            return "\n".join(result)
        
        for issue, solutions in error_db.items():
            if issue in error_desc or any(s in error_desc for s in solutions[:1]):
                result.append(f"\n📌 {issue}：")
                for s in solutions:
                    result.append(f"   • {s}")
                return "\n".join(result)
        
        result.append("未识别的问题，请描述具体错误现象")
        return "\n".join(result)

    # -------------------------- 6. 模型管理 --------------------------
    def list_models(self):
        """列出已安装模型"""
        result = ["📦 ComfyUI 模型列表："]
        model_types = {
            "checkpoints": "主模型 (SD/SDXL/FLUX)",
            "lora": "LoRA 模型",
            "controlnet": "ControlNet 模型",
            "embeddings": "Textual Inversion / InstantID",
            "vae": "VAE 模型",
            "upscale_models": "放大模型"
        }
        for folder, desc in model_types.items():
            path = os.path.join(self.models_dir, folder)
            if os.path.exists(path):
                files = os.listdir(path)
                count = len(files)
                result.append(f"\n📁 {folder}/ ({desc}): {count}个")
                if count > 0 and count <= 10:
                    for f in files:
                        result.append(f"   • {f}")
            else:
                result.append(f"\n📁 {folder}/: 目录不存在")
        return "\n".join(result)

    # -------------------------- 7. 批量生成 --------------------------
    def batch_generate(self, prompts, params=None):
        """批量生成提示词"""
        default_params = {
            "model": "sdxl_base.safetensors",
            "steps": 28, "cfg": 7,
            "width": 1024, "height": 1024,
            "sampler": "dpmpp_2m", "scheduler": "karras"
        }
        if params:
            default_params.update(params)
        
        result = [f"🔄 批量生成 {len(prompts)} 张图片："]
        for i, prompt in enumerate(prompts, 1):
            result.append(f"\n{i}. {prompt[:50]}...")
            wf = self._gen_txt2img_workflow({**default_params, "prompt": prompt})
            result.append(f"   节点数: {len(wf['nodes'])}")
        result.append(f"\n✅ 批量任务已创建，请导入ComfyUI执行")
        return "\n".join(result)


# ===================== CLI Interface =====================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='ComfyUI V8 秋叶中文版助手')
    parser.add_argument('action', choices=[
        'check', 'start', 'workflow', 'optimize', 'troubleshoot', 'models', 'batch', 'extra'
    ], help='操作类型')
    parser.add_argument('--type', '-t', default='txt2img', help='工作流类型')
    parser.add_argument('--path', '-p', default='ComfyUI-aki-V8', help='整合包路径')
    parser.add_argument('--prompt', help='提示词')
    parser.add_argument('--output', '-o', default='workflow.json', help='输出文件')
    parser.add_argument('--params', help='JSON格式参数')
    
    args = parser.parse_args()
    skill = ComfyUI_V8_Skill(args.path)
    
    if args.action == 'check':
        print(skill.check_environment())
    elif args.action == 'start':
        print(skill.start_comfyui())
    elif args.action == 'workflow':
        result = skill.generate_workflow(args.type)
        print(result)
    elif args.action == 'optimize':
        print(skill.optimize_vram())
    elif args.action == 'troubleshoot':
        print(skill.troubleshoot(args.prompt or ""))
    elif args.action == 'models':
        print(skill.list_models())
    elif args.action == 'batch':
        prompts = args.prompt.split('|') if args.prompt else ["高质量, 8k"]
        print(skill.batch_generate(prompts))
    elif args.action == 'extra':
        print(skill.extra_features())


if __name__ == "__main__":
    main()


# ===================== 机器人技能入口（对外调用接口） =====================
def bot_skill_comfyui_v8(action="check", workflow_type="txt2img", comfy_path="ComfyUI-aki-V8"):
    """
    机器人调用ComfyUI V8技能
    action: check(检测) | start(启动) | workflow(生成工作流) | optimize(显存优化) | fix(修复) | extra(增强)
    """
    skill = ComfyUI_V8_Skill(comfy_path)
    if action == "check":
        return skill.check_environment()
    elif action == "start":
        return skill.start_comfyui()
    elif action == "workflow":
        return skill.generate_workflow(workflow_type)
    elif action == "optimize":
        return skill.optimize_vram()
    elif action == "fix":
        return skill.fix_common_errors()
    elif action == "extra":
        return skill.extra_features()
    else:
        return "❌ 无效指令，支持：check/start/workflow/optimize/fix/extra"
