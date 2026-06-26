1. 按照OpenClaw官方配置你的飞书：https://docs.openclaw.ai/channels/feishu
2. 在https://open.feishu.cn/app/cli_a937fd6055791bca/baseinfo可以找到你的App ID和APP Secret
3. 在https://open.feishu.cn/api-explorer/cli_a937fd6055791bca?apiName=create&project=im&resource=message&version=v1可以复制你的open_id

在终端测试发送图片给飞书(注意改一下user为你的open_id以及--media为你本地的图像)
```
openclaw message send --channel feishu   --target user:你的open_id   --message "这是测试图片"   --media C:/Users/Bingo/.openclaw/workspace/skills/feishu-photo/test.png
openclaw message send --channel feishu   --target user:你的open_id   --message "这是测试视频"   --media C:/Users/Bingo/.openclaw/workspace/skills/feishu-photo/huanghou.mp4
```

目前我发现图像和视频文件都需要放到skills里面的对应目录,才能发送到飞书正确显示
- 比如你是comfyui skil，就有类似的文件夹`C:/Users/Bingo/.openclaw/workspace/skills/comfyui-my-img-gen`
- 比如你是feishu-file,就有类似的文件夹`C:/Users/Bingo/.openclaw/workspace/skills/feishu-photo`