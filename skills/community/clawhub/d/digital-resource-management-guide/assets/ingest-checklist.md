# 资源入库检查清单

## 发布前检查

### 内容质量
- [ ] 内容完整，无明显错误
- [ ] 格式统一，排版清晰
- [ ] 代码示例可运行
- [ ] 链接可访问

### 元数据
- [ ] name 字段唯一且有意义
- [ ] description 10-200字，准确描述内容
- [ ] tags 3-8个，覆盖核心主题
- [ ] author 和 created 日期已填写
- [ ] version 符合 SemVer 规范

### 安全检查
- [ ] 无敏感信息（密钥、密码、个人信息）
- [ ] 无版权争议内容
- [ ] 无恶意代码

### 文件结构
```
resource-name/
├── SKILL.md              # 必填，主文档
├── reference/           # 可选，参考资料
│   └── template.yaml
├── assets/              # 可选，附件资源
└── scripts/             # 可选，脚本工具
```

## 发布命令

```bash
# 进入资源目录
cd ./resource-name

# 发布到 ClawHub
clawhub publish . \
  --slug resource-identifier \
  --name "资源显示名称" \
  --version 1.0.0 \
  --changelog "变更说明"
```

## 发布后验证

```bash
# 检查是否发布成功
clawhub inspect resource-identifier

# 搜索验证可发现性
clawhub search "关键词"
```
