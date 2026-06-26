---
name: fastapi-flask-proxy
description: FastAPI + Flask 混合部署最佳实践。解决路由定义、API 代理等常见问题。适用于需要同时运行 FastAPI API 和 Flask 前端的场景。
metadata:
  clawdbot:
    emoji: "🔀"
    requires:
      anyBins: ["python3"]
---

# FastAPI + Flask 混合部署指南

当你需要同时运行 FastAPI 后端 API 和 Flask 前端服务时，需要注意以下关键问题。

## 架构模式

```
┌─────────────────────────────────────────┐
│              用户浏览器                  │
└─────────────────┬───────────────────────┘
                  │ :15000
                  ▼
┌─────────────────────────────────────────┐
│           Flask (端口 15000)             │
│  - 静态页面                               │
│  - API 代理 → FastAPI                    │
└─────────────────┬───────────────────────┘
                  │ 内部调用
                  ▼
┌─────────────────────────────────────────┐
│          FastAPI (端口 18000)            │
│  - REST API                              │
│  - 业务逻辑                               │
└─────────────────────────────────────────┘
```

## 核心踩坑与解决方案

### 1. FastAPI 路由定义位置 ⚠️

**问题**: 路由定义在 `if __name__ == "__main__":` 之后，导致路由未被注册。

**错误示例**:
```python
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18000)

# ❌ 路由定义在 main 之后，不会被加载！
@app.get("/api/hello")
def hello():
    return {"message": "Hello"}
```

**正确示例**:
```python
from fastapi import FastAPI

app = FastAPI()

# ✅ 路由定义在 main 之前
@app.get("/api/hello")
def hello():
    return {"message": "Hello"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18000)
```

### 2. Flask API 代理 ⚠️

**问题**: 前端通过 Flask (15000端口) 访问，但 API 在 FastAPI (18000端口)，存在跨域问题。

**解决方案**: 在 Flask 中添加 API 代理。

```python
from flask import Flask, request, Response
import requests

app = Flask(__name__)
FASTAPI_BASE = "http://localhost:18000"

# 代理 GET 请求
@app.route("/api/<path:path>", methods=["GET"])
def proxy_get(path):
    resp = requests.get(f"{FASTAPI_BASE}/api/{path}", params=request.args)
    return Response(resp.content, status=resp.status_code, 
                   headers={"Content-Type": "application/json"})

# 代理 POST 请求
@app.route("/api/<path:path>", methods=["POST"])
def proxy_post(path):
    resp = requests.post(f"{FASTAPI_BASE}/api/{path}", 
                        json=request.get_json())
    return Response(resp.content, status=resp.status_code,
                   headers={"Content-Type": "application/json"})

# 代理 DELETE 请求
@app.route("/api/<path:path>", methods=["DELETE"])
def proxy_delete(path):
    resp = requests.delete(f"{FASTAPI_BASE}/api/{path}")
    return Response(resp.content, status=resp.status_code,
                   headers={"Content-Type": "application/json"})

# 代理 PUT 请求
@app.route("/api/<path:path>", methods=["PUT"])
def proxy_put(path):
    resp = requests.put(f"{FASTAPI_BASE}/api/{path}", 
                       json=request.get_json())
    return Response(resp.content, status=resp.status_code,
                   headers={"Content-Type": "application/json"})
```

### 3. 导入问题 ⚠️

**问题**: 新增的模型类在路由文件中未导入，导致 `NameError`。

**解决方案**: 确保所有使用的类都已导入。

```python
# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Trajectory(Base):
    __tablename__ = "trajectories"
    id = Column(Integer, primary_key=True)
    # ...

class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True)
    trajectory_id = Column(Integer, ForeignKey("trajectories.id"))
    # ...
```

```python
# main.py (FastAPI)
from models import Trajectory, Annotation, Response, Prompt  # ✅ 全部导入

@app.delete("/api/trajectories/{trajectory_id}")
def delete_trajectory(trajectory_id: int, db: Session = Depends(get_db)):
    # 现在可以正确访问所有模型
    annotation = db.query(Annotation).filter(
        Annotation.trajectory_id == trajectory_id
    ).first()
    # ...
```

### 4. 删除操作的级联处理

**问题**: 删除主记录时，关联的外键记录如何处理？

**方案 A**: 数据库级联删除（推荐）
```python
class Trajectory(Base):
    __tablename__ = "trajectories"
    id = Column(Integer, primary_key=True)
    annotations = relationship("Annotation", cascade="all, delete-orphan")
```

**方案 B**: 手动删除关联记录
```python
@app.delete("/api/trajectories/{trajectory_id}")
def delete_trajectory(trajectory_id: int, db: Session = Depends(get_db)):
    # 先删除关联的 annotations
    db.query(Annotation).filter(
        Annotation.trajectory_id == trajectory_id
    ).delete()
    # 再删除主记录
    trajectory = db.query(Trajectory).filter(
        Trajectory.id == trajectory_id
    ).first()
    if trajectory:
        db.delete(trajectory)
        db.commit()
    return {"status": "deleted"}
```

## 完整启动脚本

```bash
#!/bin/bash

# 启动 FastAPI 后端 (后台运行)
cd /app
python -m uvicorn api:app --host 0.0.0.0 --port 18000 &
FASTAPI_PID=$!

# 启动 Flask 前端
python frontend.py

# 清理
kill $FASTAPI_PID 2>/dev/null
```

## Docker Compose 配置

```yaml
version: '3.8'
services:
  api:
    build: .
    command: python -m uvicorn api:app --host 0.0.0.0 --port 18000
    ports:
      - "18000:18000"
    
  web:
    build: .
    command: python frontend.py
    ports:
      - "15000:15000"
    depends_on:
      - api
    environment:
      - FASTAPI_URL=http://api:18000
```

## 最佳实践总结

1. **路由定义**: 始终在 `if __name__ == "__main__":` 之前定义所有路由
2. **API 代理**: 前端服务需要代理 API 请求到后端
3. **导入管理**: 新增模型类后，确保在所有使用的地方导入
4. **级联删除**: 设计好外键关系的级联策略
5. **错误处理**: 代理请求时正确传递错误状态码

## 相关项目

- Preference Alignment System: `wphu@gpu506.aibee.cn:/data/algorithm/user/wphu/OmniMLLM/preference-align`