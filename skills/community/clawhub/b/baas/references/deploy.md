## 部署上线

> ⚠️ **部署前必须询问用户确认**，得到明确同意后再执行打包和部署操作。

### 打包策略

根据项目类型选择对应的打包方式：

**纯 HTML 项目（无构建步骤）**：

```bash
cd <项目目录>
zip -r project.zip . -x "node_modules/*" -x ".git/*" -x "*.zip"
```

**Vue/React 等需要构建的项目**：

```bash
cd <项目目录>
# 1. 执行构建
npm run build  # 或 yarn build

cd dist   # 或 cd build
zip -r ../project.zip .
```

### 执行部署

```bash
baas -c ./baas-config.json deploy ./project.zip
```

部署成功后返回：

```json
{
  "code": 0,
  "data": {
    "url": "http://localhost:8080/14217"
  },
  "message": "ok",
  "success": true
}
```