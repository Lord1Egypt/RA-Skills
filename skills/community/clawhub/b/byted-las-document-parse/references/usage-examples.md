# 使用示例 & 代码集成

## Agent 交互场景最佳实践（非阻塞异步）

✅ **推荐用法**：提交任务后立即响应用户，后台使用 `check-and-notify --poll` 自动处理落盘和通知：

```python
import subprocess
import json

def parse_document_async(file_path_or_url, output_dir="/tmp/las_parse_results"):
    # Step 1: 提交任务获取 task_id
    submit_result = subprocess.run([
        "python3", "skills/byted-las-document-parse/scripts/skill.py",
        "submit",
        "--url", file_path_or_url
    ], capture_output=True, text=True)

    if submit_result.returncode != 0:
        return f"❌ 任务提交失败: {submit_result.stderr}"

    res_json = json.loads(submit_result.stdout)
    task_id = res_json["task_id"]

    # Step 2: 启动后台子代理或独立进程执行 check-and-notify
    # 脚本内部会自动轮询、下载图片、保存结果
    poll_cmd = [
        "python3", "skills/byted-las-document-parse/scripts/skill.py",
        "check-and-notify",
        "--task-id", task_id,
        "--output", f"{output_dir}/{task_id}",
        "--poll"
    ]
    
    subprocess.Popen(poll_cmd, start_new_session=True)

    return f"✅ 解析任务已提交，任务ID: {task_id}\n🔄 后台正在自动处理，完成后将通知您。"
```

## 命令行使用示例

### 提交任务
```bash
python3 scripts/skill.py submit --url "/path/to/file.pdf"
# 返回: {"task_id": "task_123...", "eta": "1-2分钟", "input_type": "pdf"}
```

### 轮询并保存结果（Agent 核心命令）
```bash
python3 scripts/skill.py check-and-notify --task-id task_123... --output /tmp/result_dir --poll
# 成功后会在 /tmp/result_dir 生成规范的 Markdown、图片和完整 JSON
```

### 长图智能裁剪
对于长宽比 < 0.334 的长图，支持使用 LAS 多模态模型智能识别分页位置：

```bash
python3 scripts/skill.py submit --url "/path/to/long_image.png" --use-llm
```

## 本地文件自动处理
提供本地文件路径时，脚本自动完成：
1. 检测文件类型（PDF 或图片）
2. 图片检测：长截图自动分页 → 转换为 PDF
3. 自动使用配置的凭证上传到 TOS
4. 自动提交解析任务

---

## 附录：离线脚本同步用法
仅适合无需用户交互的离线脚本场景：

```python
import subprocess
import json

def parse_document_sync(file_path_or_url, output_dir):
    # 1. 提交
    submit_res = subprocess.run(["python3", "scripts/skill.py", "submit", "--url", file_path_or_url], capture_output=True, text=True)
    task_id = json.loads(submit_res.stdout)["task_id"]

    # 2. 等待并保存
    # --poll 会阻塞直到任务终态
    check_res = subprocess.run([
        "python3", "scripts/skill.py", "check-and-notify",
        "--task-id", task_id,
        "--output", output_dir,
        "--poll"
    ], capture_output=True, text=True)
    
    return json.loads(check_res.stdout)
```
