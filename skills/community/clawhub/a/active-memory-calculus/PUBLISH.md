# 发布指南 - Publish to ClawHub

## 前置要求

1. **ClawHub 账号**: 访问 https://clawhub.ai 并注册/登录
2. **ClawHub CLI 安装**:
   ```bash
   npm install -g @clawhub/cli
   ```
3. **登录验证**:
   ```bash
   clawhub login
   clawhub whoami
   ```

## 发布方式

### 方式一: CLI 直接发布（推荐）

```bash
# 进入 Skill 目录
cd /path/to/active-memory-calculus

# 发布到 ClawHub
clawhub publish . \
  --slug active-memory-calculus \
  --name "Active Memory for Calculus Teaching" \
  --version 1.0.0 \
  --changelog "Initial release: Active Memory and Dreaming System for calculus education"
```

**参数说明**:
- `--slug`: Skill 的唯一标识符（小写，用连字符分隔）
- `--name`: 显示名称
- `--version`: 版本号（遵循语义化版本）
- `--changelog`: 更新日志

### 方式二: Web 界面上传

1. 访问 https://clawhub.ai/publish-skill
2. 确保已登录（显示用户名）
3. 填写表单:
   - **Slug**: `active-memory-calculus`
   - **Display Name**: `Active Memory for Calculus Teaching`
   - **Version**: `1.0.0`
4. 点击 "Choose folder" 选择 `active-memory-calculus` 目录
5. 等待验证（识别 SKILL.md）
6. (可选) 添加 Changelog
7. 点击 "Publish skill"
8. 保存返回的 URL

## 发布前检查清单

### 文件完整性检查

```bash
# 确保所有必要文件存在
ls -la active-memory-calculus/
# 应有: SKILL.md, hermes.config.yaml, _meta.json, README.md

ls -la active-memory-calculus/tools/
# 应有: memory_extract.py, memory_apply.py, dream_generator.py, knowledge_graph.py

ls -la active-memory-calculus/prompts/
# 应有: system.md

ls -la active-memory-calculus/examples/
# 应有: example_basic_usage.md, example_integration.md, example_dream_output.md
```

### 内容检查

- [ ] `SKILL.md` 中的 `description` 字段为英文
- [ ] 无个人敏感信息（路径、账号、密钥）
- [ ] 版本号已更新
- [ ] 所有工具脚本可执行权限已设置

### 本地测试

```bash
# 测试工具脚本
python3 tools/memory_extract.py test_transcript.txt
python3 tools/memory_apply.py "求极限" student_001

# 验证 SKILL.md 格式
clawhub test .
```

## 发布后验证

### 1. CLI 验证

```bash
# 检查已发布的 Skill
clawhub inspect active-memory-calculus --json
```

### 2. Web 验证

访问: `https://clawhub.ai/skills/active-memory-calculus`

确认:
- 页面可正常访问
- 名称和版本号正确
- 描述完整
- 作者信息正确

### 3. 安装测试

```bash
# 从 ClawHub 安装
clawhub install active-memory-calculus

# 验证安装
openclaw skills status active-memory-calculus
```

## 版本更新流程

当需要更新 Skill 时:

1. **更新版本号**: 修改 `_meta.json` 和 `SKILL.md` 中的 `version`
2. **更新 CHANGELOG**: 在 `SKILL.md` 的 Changelog 部分添加新版本说明
3. **本地测试**: 确保修改正常工作
4. **重新发布**:
   ```bash
   clawhub publish . \
     --slug active-memory-calculus \
     --name "Active Memory for Calculus Teaching" \
     --version 1.1.0 \
     --changelog "Add new feature: knowledge graph visualization"
   ```

## 故障排除

### 登录问题

```bash
# 如果浏览器登录失败，使用 Token 登录
clawhub login --token <your_clh_token>
```

### 发布失败

1. 检查网络连接
2. 确认 `SKILL.md` 格式正确（YAML frontmatter 完整）
3. 验证 slug 是否已被占用:
   ```bash
   clawhub inspect active-memory-calculus
   ```

### 验证延迟

发布后可能需要几分钟才能在 Web 界面看到更新，这是正常的。

## 相关链接

- ClawHub 官网: https://clawhub.ai
- Skill 页面: https://clawhub.ai/skills/active-memory-calculus
- 作者页面: https://clawhub.ai/daigxok
- OpenClaw 文档: https://docs.openclaw.ai

## 联系支持

如有问题，可通过以下方式联系:
- GitHub Issues: https://github.com/daigxok/active-memory-calculus/issues
- ClawHub 社区: https://clawhub.ai/community
