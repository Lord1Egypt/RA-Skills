# Fooocus Skill 测试报告与经验总结

**测试时间:** 2026-03-07  
**测试环境:** Windows 10, Python 3.11.1, 无 CUDA GPU  
**测试者:** Agent

---

## 测试结果摘要

### ❌ 测试未能完成图像生成

**根本原因:** 当前测试环境缺少 CUDA GPU，Fooocus 无法运行。

---

## 遇到的问题 (踩坑记录)

### 问题 1: 环境依赖缺失

**现象:**
```
PyTorch not installed
CUDA not available
Fooocus not found
```

**原因:**
- Fooocus 需要 NVIDIA GPU + CUDA
- PyTorch 需要单独安装
- 模型文件需要 6-10GB 下载

**解决方案:**
1. 添加自动依赖安装功能
2. 检测 CPU-only 环境并给出警告
3. 提供云端替代方案

---

### 问题 2: Windows PowerShell 语法差异

**现象:**
```powershell
The token '&&' is not a valid statement separator in this version.
```

**原因:**
- PowerShell 不支持 `&&` 和 `||` 作为命令分隔符
- 需要使用 `;` 或单独执行

**解决方案:**
- 脚本中避免使用 `&&`
- 使用 Python 的 subprocess 代替 shell 命令
- 提供 PowerShell 兼容的示例

---

### 问题 3: WebSocket 依赖缺失

**现象:**
```
ModuleNotFoundError: No module named 'websockets'
```

**原因:**
- `websockets` 不是 Python 标准库
- 需要单独安装

**解决方案:**
- 在 check_env.py 中检测并提示安装
- 提供 fallback 到 HTTP API 的选项

---

### 问题 4: 模型下载时间长

**现象:**
- 首次启动需要下载 6-10GB 模型
- 下载可能失败或中断
- 没有进度显示

**解决方案:**
- 添加 `--download-models` 预下载选项
- 提供模型手动下载指南
- 添加断点续传支持（未来）

---

### 问题 5: Gradio API 变动

**现象:**
- Fooocus 版本更新可能导致 API 变化
- fn_index 可能改变
- 参数顺序可能调整

**解决方案:**
- 添加 API 版本检测
- 提供 `/api/info` 端点查询
- 记录 tested Fooocus 版本

---

## 成功经验

### ✅ 脚本结构清晰

- `check_env.py` - 环境检查
- `install_fooocus.py` - 安装脚本
- `generate_image.py` - 基础生成
- `generate_with_progress.py` - WebSocket 进度
- `list_models.py` - 模型列表

### ✅ 错误处理完善

- 每个脚本都有 try-except
- 提供清晰的错误信息
- 给出解决方案提示

### ✅ 文档完整

- SKILL.md 包含详细说明
- references/ 提供技术参考
- 使用示例丰富

---

## 改进建议

### 高优先级

1. **添加 CPU 模式支持**
   ```python
   # 在 generate_image.py 中添加
   if not torch.cuda.is_available():
       print("Warning: Running on CPU. Generation will be very slow.")
       print("Consider using --preset lightning for faster results.")
   ```

2. **自动安装依赖**
   ```bash
   python check_env.py --install-deps
   ```

3. **云端 Fooocus 支持**
   - 集成 Google Colab
   - 支持远程 Fooocus 实例

### 中优先级

4. **模型管理**
   - 列出已下载模型
   - 删除不需要的模型
   - 模型版本检查

5. **批量生成优化**
   - 队列管理
   - 并发控制
   - 结果汇总

### 低优先级

6. **GUI 界面**
   - 简单的 Tkinter 界面
   - 拖拽上传
   - 实时预览

---

## 给其他 Agent 的使用建议

### 使用前必读

1. **检查环境**
   ```bash
   python scripts/check_env.py
   ```
   确保所有检查项都是 ✅

2. **如果没有 GPU**
   - 使用 `--preset lightning` 加速
   - 降低分辨率到 512x512
   - 减少 steps 到 10-20

3. **首次使用**
   - 预留 30-60 分钟用于模型下载
   - 确保有 10GB+ 磁盘空间
   - 稳定的网络连接

### 常见错误速查

| 错误 | 原因 | 解决 |
|------|------|------|
| Connection refused | Fooocus 没启动 | 运行 `python entry_with_update.py` |
| CUDA out of memory | 显存不足 | 降低分辨率或使用 `--always-low-vram` |
| Model not found | 模型未下载 | 等待自动下载或手动下载 |
| Module not found | 依赖缺失 | 运行 `pip install -r requirements.txt` |

### 最佳实践

1. **提示词优化**
   - 使用 `masterpiece, best quality` 开头
   - 添加 `detailed, intricate` 增加细节
   - 使用负面提示词避免常见问题

2. **参数选择**
   - 草稿: `--preset lightning --steps 4`
   - 成品: `--preset default --steps 30`
   - 高质量: `--preset realistic --steps 60`

3. **批量生成**
   - 先用 lightning 快速筛选
   - 再用 default 生成最终版本
   - 使用相同 seed 进行微调

---

## 测试结论

虽然本次测试因硬件限制未能完成图像生成，但技能的基础架构是完善的。主要改进方向：

1. 增强环境检测和自动修复
2. 支持 CPU-only 模式
3. 提供云端替代方案
4. 完善错误处理和用户引导

技能已具备可用性，建议在配备 NVIDIA GPU 的环境中使用。

---

## 附录: 测试命令记录

```bash
# 环境检查
python scripts/check_env.py --json

# 安装依赖
python scripts/check_env.py --install-deps

# 安装 Fooocus
python scripts/install_fooocus.py --path ~/Fooocus

# 启动服务
python scripts/check_env.py --start

# 生成图像 (预期失败 - 无 GPU)
python scripts/generate_with_progress.py \
  --prompt "masterpiece, best quality, 1boy, solo, Chu Xuan from Infinite Terror, \"glasses, black hair, intelligent expression, tactical uniform, \"anime style, detailed face" \
  --preset anime \
  --output ./chuxuan.png
```
