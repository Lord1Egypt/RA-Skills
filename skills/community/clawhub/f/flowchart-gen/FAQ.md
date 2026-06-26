# 📚 流程图生成技能 - 常见问题解答 (FAQ)

## 目录
1. [安装问题](#安装问题)
2. [Mermaid CLI 问题](#mermaid-cli-问题)
3. [语法错误](#语法错误)
4. [DeepSeek API 问题](#deepseek-api-问题)
5. [性能问题](#性能问题)
6. [其他问题](#其他问题)

---

## 安装问题

### Q1: 如何安装流程图生成技能所需的所有依赖？

**A:**
```bash
# 1. 安装Python依赖
pip install requests pillow

# 2. 安装Node.js（如果尚未安装）
# 访问 https://nodejs.org/ 下载安装

# 3. 安装Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 4. 验证安装
mmdc --version
python -c "import requests; print('requests OK')"
python -c "from PIL import Image; print('PIL OK')"
```

### Q2: Windows系统安装遇到问题怎么办？

**A:**
Windows常见问题及解决方案：

1. **Node.js安装问题**
   - 以管理员身份运行命令提示符
   - 确保Node.js已添加到PATH
   - 重启计算机使环境变量生效

2. **Mermaid CLI命令找不到**
   - 尝试使用 `mmdc.cmd` 代替 `mmdc`
   - 检查Node.js全局安装路径是否在PATH中
   - 重新安装: `npm uninstall -g @mermaid-js/mermaid-cli && npm install -g @mermaid-js/mermaid-cli`

3. **权限问题**
   - 以管理员身份运行PowerShell/CMD
   - 检查杀毒软件是否阻止了安装

### Q3: 网络问题导致npm安装失败怎么办？

**A:**
```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install -g @mermaid-js/mermaid-cli

# 安装完成后恢复默认源（可选）
npm config set registry https://registry.npmjs.org
```

---

## Mermaid CLI 问题

### Q4: 错误 "Command 'mmdc' not found" 或 "mmdc不是内部或外部命令"

**A:**
1. **检查安装**
   ```bash
   npm list -g @mermaid-js/mermaid-cli
   ```

2. **手动查找**
   ```bash
   # Windows
   where mmdc
   where mmdc.cmd
   
   # Linux/macOS
   which mmdc
   ```

3. **重新安装**
   ```bash
   npm uninstall -g @mermaid-js/mermaid-cli
   npm install -g @mermaid-js/mermaid-cli
   ```

### Q5: Puppeteer/Chrome 相关错误

**A:**
这些错误通常是因为Mermaid CLI需要Chrome来渲染图表。

**解决方案:**
1. **安装Chrome浏览器** - 确保已安装最新版Chrome
2. **设置Chrome路径**（如果Chrome不在默认位置）:
   ```bash
   # Windows
   set PUPPETEER_EXECUTABLE_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
   
   # macOS
   export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   ```
3. **使用SVG格式**（不需要Chrome）:
   ```bash
   python scripts/generate.py "你的描述" -o output.svg -f svg
   ```

### Q6: Mermaid渲染超时（30秒）

**A:**
图表可能过于复杂或Mermaid版本有问题。

**解决方案:**
1. **简化图表** - 减少节点和边
2. **升级Mermaid CLI**
   ```bash
   npm update -g @mermaid-js/mermaid-cli
   ```
3. **使用在线工具调试** - https://mermaid.live
4. **分步生成** - 将复杂图表分解为多个简单图表

---

## 语法错误

### Q7: 如何调试Mermaid语法错误？

**A:**
1. **使用在线编辑器**
   - https://mermaid.live
   - 粘贴生成的Mermaid代码进行调试

2. **简化测试**
   ```bash
   python scripts/generate.py --raw "graph TD; A[开始]-->B[结束]" -o test.png --verbose
   ```

3. **常见语法问题**
   - 确保箭头正确: `-->` 或 `->`
   - 节点标签用方括号: `A[标签]`
   - 判断节点用花括号: `B{条件}`
   - 结束语句用分号（某些语法需要）

### Q8: AI生成的Mermaid代码有语法错误怎么办？

**A:**
1. **使用模板匹配**（禁用AI）:
   ```bash
   python scripts/generate.py "用户登录流程" --no-llm -o output.png
   ```

2. **手动修正**:
   ```bash
   python scripts/generate.py --raw "你的Mermaid代码" -o output.png
   ```

3. **提供更详细的描述** - AI需要清晰的指令
4. **使用特定模板**:
   ```bash
   python scripts/generate.py --use-template login -o output.png
   ```

---

## DeepSeek API 问题

### Q9: 如何配置DeepSeek API？

**A:**
1. **自动配置** - 脚本会自动从OpenClaw配置文件读取
   - 配置文件路径: `~/.openclaw/openclaw.json`
   - 需要包含DeepSeek API密钥配置

2. **手动配置**（环境变量）:
   ```bash
   # Windows (CMD)
   set DEEPSEEK_API_KEY=your_api_key_here
   
   # Windows (PowerShell)
   $env:DEEPSEEK_API_KEY="your_api_key_here"
   
   # Linux/macOS
   export DEEPSEEK_API_KEY="your_api_key_here"
   ```

### Q10: API调用失败或超时

**A:**
1. **检查网络连接**
2. **验证API密钥**
3. **使用模板匹配**（临时解决方案）:
   ```bash
   python scripts/generate.py "你的描述" --no-llm -o output.png
   ```
4. **检查OpenClaw配置**
   ```bash
   # 查看配置状态
   python scripts/generate.py "测试" --verbose
   ```

---

## 性能问题

### Q11: 图表生成太慢怎么办？

**A:**
**优化建议:**
1. **简化图表** - 减少复杂度
2. **使用SVG格式** - 比PNG生成更快
   ```bash
   python scripts/generate.py "描述" -o output.svg -f svg
   ```
3. **禁用AI生成** - 使用模板匹配
   ```bash
   python scripts/generate.py "描述" --no-llm -o output.png
   ```
4. **预生成模板** - 对于重复使用的图表

### Q12: 内存占用过高

**A:**
1. **降低图表复杂度**
2. **增加超时时间**（在代码中修改）
3. **分批处理** - 将大型项目分解
4. **使用简单图像模式**（当Mermaid不可用时自动启用）

---

## 其他问题

### Q13: 如何贡献新的模板？

**A:**
1. 编辑 `scripts/generate.py` 文件
2. 在 `TEMPLATES` 字典中添加新模板
3. 在 `template_keywords` 中添加关键词映射
4. 测试新模板
5. 提交Pull Request

**模板格式:**
```python
"template-name": """graph TD
    A[节点1] --> B[节点2]
    B --> C[节点3]""",
```

### Q14: 如何报告bug或请求功能？

**A:**
1. **收集信息**
   - 错误消息
   - 使用的命令
   - 操作系统和版本
   - Python和Node.js版本

2. **重现步骤**
   - 详细说明如何重现问题
   - 提供最小复现示例

3. **创建issue**
   - 在GitHub仓库创建issue
   - 提供收集的所有信息

### Q15: 如何使用其他Mermaid图表类型？

**A:**
目前支持的图表类型:
- 流程图 (`graph TD` / `graph LR`)
- 序列图 (`sequenceDiagram`)
- 甘特图 (`gantt`)
- 类图 (`classDiagram`)
- 状态图 (`stateDiagram-v2`)
- 饼图 (`pie`)
- 用户旅程图 (`journey`)
- 时间线图 (`timeline`)

**使用示例:**
```bash
# 甘特图
python scripts/generate.py "项目时间计划" -o gantt.png

# 类图  
python scripts/generate.py "系统类图设计" -o class.png

# 状态图
python scripts/generate.py "状态机设计" -o state.png
```

---

## 📞 获取帮助

### 快速诊断
```bash
# 运行诊断命令
python scripts/diagnose.py

# 检查环境
python -c "import sys; print(f'Python: {sys.version}')"
node --version
mmdc --version
```

### 在线资源
- **Mermaid官方文档**: https://mermaid.js.org
- **在线编辑器**: https://mermaid.live  
- **语法参考**: https://mermaid.js.org/syntax/flowchart.html
- **OpenClaw文档**: https://docs.openclaw.ai

### 社区支持
- **Discord社区**: https://discord.com/invite/clawd
- **GitHub Issues**: 报告bug和请求功能
- **文档贡献**: 帮助改进文档

---

**最后更新**: 2026-03-17  
**版本**: 流程图生成技能 v1.0