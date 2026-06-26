# ClawHub 国内镜像验证记录

## 镜像地址
- **国内镜像**: `https://cn.clawhub-mirror.com`
- **官方地址**: `https://clawhub.ai`

## 环境变量配置

在 `~/.bashrc` 中添加：
```bash
# ClawHub 国内镜像配置
export CLAWHUB_REGISTRY=https://cn.clawhub-mirror.com
export CLAWHUB_SITE=https://cn.clawhub-mirror.com
```

执行 `source ~/.bashrc` 使当前会话生效。

## 验证结果

执行 `clawhub search "git"` 测试结果：

| 技能名称 | 评分 |
|----------|------|
| git-essentials | 3.784 |
| git-workflows | 3.724 |
| git-helper | 3.633 |

## CLI 版本
- ClawHub CLI v0.6.1

## 备选配置文件

如需全局配置，可在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "clawhub": {
    "registry": "https://cn.clawhub-mirror.com",
    "site": "https://cn.clawhub-mirror.com"
  }
}
```

## 临时使用参数

单次命令使用镜像：
```bash
clawhub install <skill-slug> --registry https://cn.clawhub-mirror.com
```
