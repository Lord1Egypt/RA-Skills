---
name: baidu-search-CLI
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["shell"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---
# Baidu Search
通过百度AI搜索API搜索网络，但不需要安装python,直接改用CLI
## Usage
1.curl命令，发送的post json请参考当前目录下的search_request.json文件  
2.用户的系统如果是windows请用cmd执行curl命令，不要用PowerShell  
3.如果环境变量BAIDU_API_KEY不存在，返回信息:没有获取到环境变量BAIDU_API_KEY，请搜索如何获取BAIDU_API_KEY  
4.如果环境变量BAIDU_API_KEY存在但curl返回身份验证错误,返回信息:APIKEY验证失败，请检查你的环境APIKEY是否设置正确  
```bash  

curl -X POST -H "Authorization: Bearer apikey" -H "X-Appbuilder-From: openclaw" -H "Content-Type: application/json" -d "@search_request.json" "https://qianfan.baidubce.com/v2/ai_search/web_search"
```
## Request Param  

apikey     desc:从环境变量BAIDU_API_KEY中获取apikey    
下面几个参数是search_request.json的字段说明  
content:string    desc:Search query  
top_k:int         desc:返回的数据条数，默认为10条，最多50条  
gte:string        desc:消息的开始时间，格式为"YYYY-MM-DD"  
lt:string         desc:消息的结束时间，格式为"YYYY-MM-DD"
