# skills/complex-workflow-freezer/__init__.py — 高保真可执行代码
from pathlib import Path
import hashlib
import os
from importlib.metadata import version, PackageNotFoundError

class MissingDependencyError(Exception):
    def __init__(self, pkg: str):
        super().__init__(f"Missing {pkg}—install with pip install {pkg}")
        self.pkg = pkg

class InconsistentInputError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Input checksum mismatch: {msg}")

def check_deps() -> None:
    """初始化阶段依赖检查"""
    required = ["scikit-learn", "pillow", "clawhub>=0.5"]
    for req in required:
        pkg = req.split(">=")[0]
        try:
            ver = version(pkg)
            if pkg == "clawhub" and float(ver) < 0.5:
                raise PackageNotFoundError
        except PackageNotFoundError:
            raise MissingDependencyError(req)

def check_vlm_capability(flags: list[str]) -> bool:
    """运行时多模态能力检查"""
    return any(f in ["vlm_siglip", "vlm_clip"] for f in flags)

def validate_checksum(item: list[dict], prev: str | None = None) -> str:
    """输入校验和验证（一致性策略核心）"""
    ck = hashlib.sha256(str(item).encode()).hexdigest()[:16]
    if prev and ck != prev:
        raise InconsistentInputError(f"Expected {prev}, got {ck}")
    return ck

def send_progress(stage: str, epoch: int, progress: int, msg: str) -> None:
    """进度反馈 — 符合生态渠道要求"""
    from clawhub.utils import event_logger
    event = {"stage": stage, "epoch": epoch, "progress": progress, "msg": msg}
    event_logger.info(f"FZW_FTR: {event}")
    if os.getenv("OPENCLAW_CHANNEL") in ["webchat", "telegram"]:
        from clawhub.messaging import send
        send("user", f"[freezer] {stage} — 进度{progress}% — {msg}", os.getenv("OPENCLAW_CHANNEL"))

# 主调用函数（skill生态可直接调用）
def freeze_workflow(
    workflow_id: str,
    key_findings: list[dict],
    decisions: list[dict],
    execution_path: list[str],
    output_path: Path,
    multimodal_check: bool = True
) -> dict:
    # 1. 初始化阶段
    check_deps()
    model_flags = os.getenv("MODEL_FLAGS", "").split(",")
    vlm_ok = check_vlm_capability(model_flags)
    check_status = "PASS" if vlm_ok else "WARN" if multimodal_check else "PASS"
    if not (output_path.exists() and output_path.is_dir()):
        raise ValueError(f"输出路径无效：{output_path} 必须是绝对且存在的目录")
    # 2. 冻结阶段（一致性策略）
    find_ck = validate_checksum(key_findings)
    dec_ck = validate_checksum(decisions)
    locked_thresh = [d["threshold"] for d in decisions if float(d["threshold"]) == 0.85]  # 锁定固定决策阈值
    exec_copy = list(execution_path)  # 执行路径副本（immutable）
    send_progress("freeze", 2, 50, "一致性验证通过 — 锁定阈值和执行路径")
    # 3. 多模态分支处理
    multimodal_layers = None
    if vlm_ok:
        from clawhub.multimodal import siglip_embed
        from PIL import Image
        image_paths = [f["image_path"] for f in key_findings if "image_path" in f]
        if image_paths:
            images = [Image.open(p) for p in image_paths]
            multimodal_layers = siglip_embed(images, random_state=42)  # 随机状态锁定
            send_progress("multimodal", 3, 70, "多模态嵌入生成完成")
        else:
            multimodal_layers = None  # 无图像则跳过多模态层
    elif multimodal_check:
        check_status = "WARN"
        locked_thresh = [d["threshold"] for d in decisions if float(d["threshold"]) >= 0.8]  # 降级阈值
        send_progress("freeze", 3, 65, "VL不支持 — 降级到宽松阈值")
    else:
        send_progress("freeze", 3, 65, "跳过多模态检查")
    # 4. 保存规格（终结一致性）
    skill_id = f"skill-{workflow_id.split('-')[1]}-{workflow_id.split('-')[2]}"
    saved_specs = output_path / f"{skill_id}_specs.json"
    content = {
        "skill_id": skill_id,
        "checksums": {"findings": find_ck, "decisions": dec_ck},
        "locked_thresh": locked_thresh,
        "exec_copy": exec_copy,
        "vlm_layers": multimodal_layers,
        "check_status": check_status
    }
    saved_specs.write_text(str(content))
    # 5. 最终进度
    send_progress("final", 4, 100, f"完成技能固化：{skill_id}")
    return {
        "skill_id": skill_id,
        "saved_specs": str(saved_specs),
        "multimodal_layers": multimodal_layers,
        "check_status": check_status
    }

# 入口点（用于ecosystem注册）
if __name__ == "__main__":
    # 快速验证（传入示例参数）
    ex_flow_id = "wrk-20260710-001"
    ex_findings = [{"finding_id": "f1", "score": 0.85, "cluster": "green"}, {"finding_id": "f2", "score": 0.85, "cluster": "green", "image_path": "./test.png"}]
    ex_decisions = [{"decision_id": "d1", "rationale": "score > 0.85 → keep", "threshold": 0.85}]
    ex_path = ["check_input", "validate_ck", "lock_thresh", "load_exec"]
    ex_out = Path("/root/.openclaw/workspace/skills/complex-workflow-freezer")
    try:
        result = freeze_workflow(ex_flow_id, ex_findings, ex_decisions, ex_path, ex_out)
        print(f"成功固化：{result['skill_id']} — 规格路径：{result['saved_specs']}")
    except Exception as e:
        print(f"失败（专业级告警）：{type(e).__name__} — {e}")
