# boc-init skill

BOC 3.10 部署机初始化工具。

## 目录结构

```
boc-init/
├── SKILL.md           # 技能定义文件
├── scripts/
│   └── boc_init.js    # 自动化初始化脚本
└── references/        # 参考文档目录(预留)
```

## 使用方式

调用此技能时，需要提供以下参数：
- 部署包目录
- 部署包文件名
- 部署机IP
- SSH端口
- SSH用户名
- SSH密码

技能会自动完成：
1. 环境检查
2. 部署包SHA256校验
3. 解压部署包
4. 执行 bocctl init 初始化
5. 验证初始化结果