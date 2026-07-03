# 4 文件模板规范

## skill.yaml（元数据）

```yaml
meta:
  id: {skill-id}
  name: {skill_name}
  v: {version}
  d: {desc}
  src: {github|registry|custom|api}
  tags: [t1,t2,t3]
  pf: [universal]

schema:
  in: {input_json_schema}
  out: {output_json_schema}

props:
  dom: {domain}
  mode: {mode}
  lvl: {complexity}
  sec: safe
  st: draft

deps: []
perms: []
```

YAML 键名压缩规则：
- `meta` → `meta`（保留，核心命名空间）
- `name` → `name`（保留，接口名）
- `version` → `v`
- `description` → `d`
- `source` → `src`
- `tags` → `tags`（保留）
- `platforms` → `pf`
- `schema/input` → `schema.in`
- `schema/output` → `schema.out`
- `properties/domain` → `props.dom`
- `properties/mode` → `props.mode`
- `properties/level` → `props.lvl`
- `properties/security` → `props.sec`
- `properties/status` → `props.st`
- `dependencies` → `deps`
- `permissions` → `perms`

## impl.py（零依赖实现）

```python
import sys,json,os,re,math,random,datetime,itertools,collections,typing,inspect,hashlib,base64,urllib.request,http.client,socket,ssl,time,uuid,string,warnings,traceback,io,csv,html

def _e(m):raise Exception(m)
def _j(d):return json.dumps(d,ensure_ascii=False,separators=(',',':'))
def _p(s):return json.loads(s)

def run(a):
    r={'s':'ok','d':None,'e':None}
    try:
        r['d']=a.get('x')
    except Exception as x:
        r['s']='err';r['e']=str(x)
    return r

if __name__=='__main__':
    run(_p(sys.argv[1]) if len(sys.argv)>1 else {})
```

Token 压缩规则：
1. 导入行：只保留实际使用的模块
2. 辅助函数：`_e`=raise, `_j`=json.dumps, `_p`=json.loads, `_h`=hash, `_t`=time, `_u`=url相关
3. 主函数：`run(a)` 固定签名，`a`=args dict
4. 返回值：`r['s']`=status, `r['d']`=data, `r['e']`=error
5. 错误处理：`try/except` 包围全部逻辑
6. 无类型提示、无文档字符串、无注释
7. 单引号优先；分号连接相关语句
8. 短路求值：`v=a.get('k')or d` 替代 if

## test.py（隔离测试）

```python
import sys,json,time,traceback,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from impl import run

class T:
    def __init__(s):
        s.p=0;s.f=0;s.c=[]
    def a(s,c,n,m=''):
        if c:s.p+=1;print(f'OK {n}')
        else:s.f+=1;s.c.append((n,m));print(f'FAIL {n}: {m}')
    def r(s,i,e,n):
        try:
            t0=time.time();o=run(i);t1=time.time()
            s.a(o['s']==e.get('s','ok'),f'{n}_s',o.get('e',''))
            if'd'in e:s.a(o.get('d')==e['d'],f'{n}_d')
            if't'in e:s.a((t1-t0)<e['t'],f'{n}_t',f'{(t1-t0)*1000:.0f}ms')
            return o
        except Exception as x:s.a(0,f'{n}_x',str(x));return None
    def x(s):
        print(f'\nP {s.p} F {s.f}')
        if s.c:print('F:',s.c);sys.exit(1)
        print('ALL_OK')
```

## manifest.json（跨生态适配声明）

```json
{
  "skill_id": "{skill-id}",
  "version": "{version}",
  "universal": {
    "entry": "run",
    "input": "dict",
    "output": "dict"
  },
  "openai_function": {
    "name": "{skill_name}",
    "description": "{desc}",
    "parameters": {input_json_schema},
    "strict": true
  },
  "claude_tool": {
    "name": "{skill_name}",
    "description": "{desc}",
    "input_schema": {input_json_schema}
  },
  "http_api": {
    "method": "POST",
    "endpoint": "/skill/{skill-id}",
    "content_type": "application/json",
    "headers": ["X-Skill-Version: {version}"]
  }
}
```

## 跨生态调用示例

### Kimi / 通用 Agent
```python
import sys;sys.path.insert(0,'registry/{skill-id}/{version}')
from impl import run
result = run({'x': 'input'})
```

### OpenAI Function
```json
{
  "name": "{skill_name}",
  "arguments": "{\"x\": \"input\"}"
}
```

### Claude Tool
```xml
<tool_use>
  <name>{skill_name}</name>
  <arguments>{"x": "input"}</arguments>
</tool_use>
```

### 通用 HTTP
```bash
curl -X POST http://agent-cluster/skill/{skill-id} \
  -H "Content-Type: application/json" \
  -H "X-Skill-Version: {version}" \
  -d '{"x": "input"}'
```
