# exec-batch-skill

## 功能
封装常用操作为可复用工具，减少exec调用

## 触发条件
当需要批量处理文件、搜索、写入时使用

## 使用方法
```python
# 读取文件
python exec-batch-skill.py read <filepath>

# 写入文件  
python exec-batch-skill.py write <filepath> <content>

# 搜索
python exec-batch-skill.py search <query>
```
