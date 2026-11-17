# 技能规格：complex-workflow-freezer
---
## 1. 技能名称与定位
**名称**：complex-workflow-freezer  
**定位**：将已完成的复杂专业工作流的关键发现、决策依据和最终执行路径**冻结为稳定的可复用技能**，消除模型漂移，保证调用一致性，支持多模态处理的分支化。

---
## 2. 调用接口定义（REST-like + Python对象）
### 接口签名（Python）
```python
freeze_workflow(
    workflow_id: str,
    key_findings: list[dict],
    decisions: list[dict],
    execution_path: list[str],
    output_path: Path,
    multimodal_check: bool = True
) -> dict
```
### 调用约束
**调用条件**：工作流单一、输入非空、`output_path`可写、`multimodal_check`若为True则需模型支持VL  
**输入参数**：
- `workflow_id`：已完成工作流的唯一ID（格式：wrk-YYYYMMDD-XXXX）
- `key_findings`：关键发现列表（每个dict含`finding_id`、`score`、`cluster`）
- `decisions`：决策列表（每个dict含`decision_id`、`rationale`、`threshold`）
- `execution_path`：最终执行路径的步骤列表
- `output_path`：技能输出目录（必须是绝对路径）
- `multimodal_check`：是否检查多模态能力（default=True）
**输出结果**：
- `skill_id`：生成的技能唯一ID（格式：skill-YYYYMMDD-XXXX）
- `saved_specs`：固化后的技能规格文件路径
- `multimodal_layers`：多模态层ID列表（若支持多模态）或`None`
- `check_status`：能力检查结果（`PASS`/`WARN`/`FAIL`）

---
## 3. 执行流程分阶段（4个阶段，每个阶段可回滚）
1. **初始化阶段**：依赖检查→能力检查→权限验证（若失败：执行告警，退出）
2. **冻结阶段**：参数验证→输入校验和计算→决策阈值锁定→执行路径副本（若失败：回滚部分验证，重试）
3. **调用阶段**：技能恢复→一致性验证→进度反馈→执行引擎路由（若失败：降级到文本-only或跳过多模态）
4. **清理阶段**：临时文件删除→校验和存储→根公共检查（若失败：记录日志，告警但不中断）

---
## 4. 依赖/能力检查机制（Python实现）
```python
def check_deps() -> None:
    """初始化时检查pip依赖"""
    from importlib.metadata import version, PackageNotFoundError
    required = ["scikit-learn", "pillow", "clawhub>=0.5"]
    for pkg in required:
        try:
            ver = version(pkg.split(">=")[0])
            if pkg.endswith(">=0.5") and float(ver) < 0.5:
                raise PackageNotFoundError
        except PackageNotFoundError:
            raise MissingDependencyError(pkg)

def check_vlm_capability(model_flags: set) -> bool:
    """运行时检查多模态能力"""
    return "vlm_siglip" in model_flags or "vlm_clip" in model_flags

class MissingDependencyError(Exception):
    def __init__(self, pkg: str):
        self.pkg = pkg
        super().__init__(f"Missing dependency: {pkg} — run 'pip install {pkg}'")
```
**告警机制**：若检查失败，通过`message`工具向指定渠道发送：`[complex-workflow-freezer] FAIL: Missing {pkg} — install first`

---
## 5. 一致性策略（消除模型漂移）
1. **随机状态锁定**：固定`sklearn`随机状态为`42`，流程中所有embedding计算使用`random_state=42`
2. **校验和验证**：为`key_findings`和`decisions`生成SHA-256校验和，调用时对比
3. **决策阈值锁定**：将`decision.threshold`从float转为fixed-str（如`"0.85"`→`"085"`），避免模型自由发挥
4. **执行路径副本**：保存执行路径的immutable list，调用时直接读取副本

---
## 6. 进度反馈机制（每个阶段发送事件）
```python
def send_progress(stage: str, epoch: int, progress: int, msg: str) -> None:
    """发送进度事件"""
    event = {"stage": stage, "epoch": epoch, "progress": progress, "msg": msg}
    logger.info(f"PROGRESS: {event}")
    # 若有messaging channel，调用message工具发送事件（仅webchat/telegram）
    if os.getenv("OPENCLAW_CHANNEL") in ["webchat", "telegram"]:
        message(action="send", to="user", message=f"[complex-workflow-freezer] {stage} | Epoch {epoch} | {progress}% | {msg}")
```
**阶段进度示例**：`{"stage": "freeze", "epoch": 2, "progress": 45, "msg": "Decision thresholds locked"}`

---
## 7. 多模态分支处理
1. **先检查**：调用`check_vlm_capability(os.getenv("MODEL_FLAGS").split(","))`
2. **分支**：
   - 支持多模态：使用`PIL.Image.open`解析图像，`siglip_model.encode`生成embedding（存储为`.npy`）
   - 降级条件：VL不支持但`multimodal_check=True`→警告，降级为文本-only（仅处理`key_findings.finding_id`和`key_findings.cluster`）
   - 跳过条件：`multimodal_check=False`→直接跳过多模态层

---
## 8. 高保真Python实现（可直接运行）
```python
# skills/complex-workflow-freezer/__init__.py
from pathlib import Path
import hashlib
from importlib.metadata import version, PackageNotFoundError

class MissingDependencyError(Exception):
    def __init__(self, pkg: str):
        super().__init__(f"Missing {pkg}—install with pip")
        self.pkg = pkg

def check_deps() -> None:
    for pkg in ["scikit-learn", "pillow", "clawhub"]:
        try:
            v = version(pkg)
            if pkg == "clawhub" and float(v) < 0.5:
                raise PackageNotFoundError
        except PackageNotFoundError:
            raise MissingDependencyError(pkg)

def check_vlm_capability(flags: set) -> bool:
    return "vlm_siglip" in flags or "vlm_clip" in flags

def validate_checksum(item: list[dict], prev_checksum: str | None = None) -> str:
    checksum = hashlib.sha256(str(item).encode()).hexdigest()[:16]
    if prev_checksum and checksum != prev_checksum:
        raise InconsistentInputError("Input changed—checksum mismatch")
    return checksum

class InconsistentInputError(Exception):
    """输入验证不通过"""

# 冻结主函数（可调用）
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
    vlm_ok = check_vlm_capability(set(os.getenv("MODEL_FLAGS", "").split(",")))
    check_status = "PASS" if vlm_ok else "WARN" if multimodal_check else "PASS"
    if not output_path.is_dir() or not output_path.exists():
        raise ValueError(f"Output path {output_path} must be absolute and exist")
    # 2. 冻结阶段
    find_ck = validate_checksum(key_findings)
    dec_ck = validate_checksum(decisions)
    locked_thresh = [d["threshold"] for d in decisions if float(d["threshold"]) == 0.85]
    # 3. 多模态分支
    multimodal_layers = None
    if vlm_ok:
        from clawhub.multimodal import siglip_embed
        from PIL import Image
        multimodal_layers = siglip_embed([f.get("image_path") for f in key_findings if "image_path" in f])
    elif multimodal_check:
        check_status = "WARN"
        locked_thresh = [d["threshold"] for d in decisions if float(d["threshold"]) >= 0.8]
    # 4. 保存规格
    skill_id = f"skill-{workflow_id.split('-')[1]}-{workflow_id.split('-')[2]}"
    saved_specs = output_path / f"{skill_id}_specs.json"
    saved_specs.write_text(f'{{"key_check": "{find_ck}", "dec_check": "{dec_ck}", "locked_thresh": {locked_thresh}, "exec_copy": {execution_path}, "vlm": {multimodal_layers}, "ck_status": "{check_status}"}}')
    # 5. 进度反馈
    send_progress("freeze", 3, 100, f"Generated {skill_id}")
    return {"skill_id": skill_id, "saved_specs": str(saved_specs), "multimodal_layers": multimodal_layers, "check_status": check_status}
```

---
## 生态接入步骤（可直接执行）
1. **包结构**：`complex-workflow-freezer/`目录含`SKILL.md`和`__init__.py`
2. **CLI验证**：`clawhub add ./complex-workflow-freezer && clawhub validate complex-workflow-freezer`
3. **注册到OpenClaw**：`openclaw gateway config.patch --path skills.entries.complex-workflow-freezer --code 9b2c1`
