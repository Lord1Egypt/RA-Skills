# FFBox AI 友好的 API 文档

本文档专为 AI 阅读优化，包含了 FFBoxService 的完整 HTTP API 接口定义、请求/响应格式、用途说明，同时保持简洁以减少 token 消耗。

## 基础信息

- **默认端口**: 33269
- **认证方式（如需）**: Bearer Token（通过 `/api/v1/auth/login` 获取）
- **Content-Type**: `application/json; charset=utf-8`
- **编码**: 优先使用 UTF-8，否则处理非英文路径时可能出错。如使用 PowerShell 等终端，请指定 UTF-8 相关参数

### 启动参数
```bash
FFBoxService 版本 5.2 - FFBox 服务端程序
如需帮助，请使用 --help 参数

Options:
  -?, -h, --help        显示 FFBoxService 帮助文档
  --port [number]       指定监听端口
  --webuiPort [number]  同时启动一个静态资源服务器以使用 webUI
  --loglevel [0|3|5|6]  信息显示级别（无|错误|事件|调试）
```

### 登录与认证

**默认情况**: 作为本地服务使用，使用空用户名、无密码，可直接发送任意 HTTP 请求，无需认证。

**有密码情况**: 若用户配置服务开放到网络，应设置密码。此情况下除 login 外的操作均需要 Bearer Token 认证。

**登录接口**:
- **URL**: `POST /api/v1/auth/login`
- **请求**:
  ```json
  {
    "username": "string",
    "passkey": "string"
  }
  ```
- **响应**:
  ```json
  {
    "isUserExist": boolean,
    "isSuccess": boolean,
    "sessionId": "string",
    "functionLevel": number
  }
  ```

## 完整 API 接口列表

### 1. 任务管理模块

#### GET /api/v1/tasks
- **用途**: 获取任务 ID 列表
- **响应**: `[1, 2, 3, ...]` (任务 ID 数组)

#### POST /api/v1/tasks
- **用途**: 创建新任务
- **请求**:
  ```json
  {
    "taskName": "string",
    "outputParams": OutputParams
  }
  ```
- **响应**:
  ```json
  {
    "taskId": number
  }
  ```

#### GET /api/v1/tasks/{id}
- **用途**: 获取单个任务详情
- **路径参数**: `id` (任务 ID)
- **响应**: `Task` 对象

#### DELETE /api/v1/tasks/{id}
- **用途**: 删除任务（支持状态: initializing, idle, idle_queued, finished, error → deleted）
- **路径参数**: `id` (任务 ID)
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/tasks/{id}/start
- **用途**: 启动单个任务（idle, idle_queued, error → running → finished/error）
- **路径参数**: `id` (任务 ID)
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/tasks/{id}/ready
- **用途**: 准备任务（加入队列，不会启动调度系统）
- **路径参数**: `id` (任务 ID)
- **状态转换**: idle, paused → idle_queued, paused_queued → running
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/tasks/{id}/pause
- **用途**: 暂停任务
- **路径参数**: `id` (任务 ID)
- **状态转换**: running, paused_queued → paused
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/tasks/{id}/resume
- **用途**: 继续执行单个任务
- **路径参数**: `id` (任务 ID)
- **状态转换**: paused, paused_queued → running
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/tasks/{id}/reset
- **用途**: 停止 | 强制停止 | 重置任务
- **路径参数**: `id` (任务 ID)
- **状态转换**: paused, paused_queued, stopping, finished, error → idle
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### PUT /api/v1/tasks/parameters
- **用途**: 批量设置任务参数
- **请求**:
  ```json
  {
    "ids": [number],
    "params": [OutputParams]
  }
  ```
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/tasks/{id}/merge-upload
- **用途**: 合并上传的文件（远程任务专用）
- **路径参数**: `id` (任务 ID)
- **请求**:
  ```json
  {
    "hashs": ["string"],
    "fileBaseName": "string",
    "inputName": "string",
    "fileTime": {
      "accessTime": number,
      "createTime": number,
      "modifyTime": number
    }
  }
  ```
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### PUT /api/v1/tasks/{id}/upload-status
- **用途**: 设置上传状态
- **路径参数**: `id` (任务 ID)
- **请求**:
  ```json
  {
    "isUploading": boolean
  }
  ```
- **响应**:
  ```json
  {
    "success": true
  }
  ```

### 2. 队列管理模块

#### POST /api/v1/queue/start
- **用途**: 启动队列（优先启动已排队任务，再将空闲任务加入排队）
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/queue/pause
- **用途**: 暂停队列（暂停运行中任务，重置已排队任务）
- **响应**:
  ```json
  {
    "success": true
  }
  ```

### 3. 系统信息模块

#### GET /api/v1/system/version
- **用途**: 获取 FFBoxService 版本号
- **认证**: 无需
- **响应**: `"5.2"` (纯文本字符串)

#### GET /api/v1/system/properties
- **用途**: 获取系统属性信息
- **响应**:
  ```json
  {
    "os": "string",
    "isSandboxed": boolean,
    "machineId": "string",
    "functionLevel": number,
    "ffmpegInfo": FFmpegInfo
  }
  ```

#### GET /api/v1/system/codecs
- **用途**: 获取已缓存的 ffmpeg 编解码器信息
- **响应**:
  ```json
  {
    "codecs": {
      "video": [FFmpegCodecDetail],
      "audio": [FFmpegCodecDetail]
    },
    "formats": {
      "muxer": [FFmpegMuxerDetail],
      "demuxer": [FFmpegDemuxerDetail]
    },
    "filters": [FFmpegFilterDetail]
  }
  ```

#### GET /api/v1/system/working-status
- **用途**: 获取工作状态（idle 或 running）
- **响应**: `"idle"` 或 `"running"` (纯文本字符串)

#### GET /api/v1/system/notifications
- **用途**: 获取通知列表
- **响应**: `[Notification]` (通知对象数组)

#### DELETE /api/v1/system/notifications/{id}
- **用途**: 删除通知
- **路径参数**: `id` (通知 ID)
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/system/settings/reload
- **用途**: 重新加载服务器配置
- **响应**:
  ```json
  {
    "success": true
  }
  ```

### 4. 文件传输模块

#### POST /api/v1/upload/check
- **用途**: 批量检查文件是否已缓存
- **请求**:
  ```json
  {
    "hashs": ["string"]
  }
  ```
- **响应**: `[1, 0, 1, ...]` (1=已缓存, 0=未缓存)

#### POST /api/v1/upload/file
- **用途**: 上传文件
- **请求**: multipart/form-data
  - `file`: 二进制文件
  - `name`: 文件名（hash）
- **响应**:
  ```json
  {
    "success": true
  }
  ```

### 5. Webhook 管理模块

#### GET /api/v1/webhooks
- **用途**: 获取所有 Webhook（不包含 secret 字段）
- **响应**: `[Webhook]` (Webhook 对象数组)

#### POST /api/v1/webhooks
- **用途**: 创建 Webhook
- **请求**: `CreateWebhookRequest`
- **响应**: `Webhook` (不包含 secret 字段)

#### GET /api/v1/webhooks/{id}
- **用途**: 获取单个 Webhook
- **路径参数**: `id` (Webhook ID)
- **响应**: `Webhook` (不包含 secret 字段)

#### PUT /api/v1/webhooks/{id}
- **用途**: 更新 Webhook
- **路径参数**: `id` (Webhook ID)
- **请求**: `UpdateWebhookRequest`
- **响应**: `Webhook` (不包含 secret 字段)

#### DELETE /api/v1/webhooks/{id}
- **用途**: 删除 Webhook
- **路径参数**: `id` (Webhook ID)
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### POST /api/v1/webhooks/{id}/test
- **用途**: 测试 Webhook 连通性
- **路径参数**: `id` (Webhook ID)
- **响应**:
  ```json
  {
    "success": boolean,
    "message": "string"
  }
  ```

### 6. 其他模块

#### POST /api/v1/activation
- **用途**: 激活 FFBoxService
- **请求**:
  ```json
  {
    "userInput": "string"
  }
  ```
- **成功响应**: 加密后的激活结果字符串
- **失败响应**:
  ```json
  {
    "error": "string"
  }
  ```

#### GET /api/v1/cache
- **用途**: 获取上传下载缓存信息
- **响应**: `CacheInfo`

#### DELETE /api/v1/cache
- **用途**: 清除上传下载缓存
- **响应**: `CacheInfo`

## 核心数据类型定义

```

/**
 * 任务信息
 */
export interface Task {
	taskName: string;
	before: InputInfo[]; // 由 ffmpeg 读取，并由 FFBox 解析完成的输入文件信息。它与 after.input.files 一一对应
	after: OutputParams;
	paraArray: Array<string>; // 由 FFBox 计算出的将要交给 ffmpeg 的指令
	status: TaskStatus;
	progressLog: {
		time: SingleProgressLog;
		frame: SingleProgressLog;
		size: SingleProgressLog;
		// 涉及到的时间单位均为 s
		lastStarted: number;
		elapsed: number; // 暂停才更新一次，因此记录的并不是实时的任务时间
		lastPaused: number; // 既用于暂停后恢复时计算速度，也用于统计任务耗时
	};
	cmdData: string; // 如果刚创建完任务，这里是 ffmpeg 读取媒体信息的结果（应有 `At least one output file must be specified`），否则是转码输出的结果
	errorInfo: Array<string>;
	// notifications: Array<Notification>;
	outputFiles: string[];		// 对于本地任务，表示生成文件的绝对路径；对于远程任务，则为 fileName（自动生成的字符串） + ext，在 taskAdd 和调节参数之后生成文件名，注意不包含目录。
}

/**
 * 输入文件配置
 * 每个 InputFile 对应一个 ffmpeg 的输入源
 */
export interface InputFile {
    /** 硬件加速方法，对应 -hwaccel 参数（如 cuda、qsv、d3d11va） */
    hwaccel?: string;
    /** 输入文件路径，对应 -i 参数后的文件路径。本地模式下直接是文件全路径，网络模式下 merge 之后获得的文件名填充到此处 */
    filePath?: string;
    /** 解复用器格式，对应 -f 参数（如 mp4、matroska、lavfi） */
    demuxer?: string;
    /** 输入起始时间点，对应 -ss 参数（置于 -i 之前为快速定位，置于 -i 之后为精确解码） */
    begin?: string;
    /** 输入结束时间点，对应 -to 参数 */
    end?: string;
    /** 是否按实时速率读取输入，对应 -re 参数（常用于推流场景） */
    realtime?: boolean;
    /** 解复用器的详细设置，对应 -demuxer_options 或 -f 选项后的参数 */
    detail?: Record<string, any>;
    /** 自定义参数，原样附加到 ffmpeg 命令中 */
    custom?: string;
}

/**
 * 滤镜图节点
 * 用于构建 ffmpeg -filter_complex 参数中的滤镜图
 */
export interface FilterNode {
    /** 节点唯一标识 */
    id: number;
    /** 滤镜名称：滤镜节点为滤镜名（如 scale、overlay）；输入节点为 in_N；输出节点为 out_N */
    name: string;
    /** 滤镜参数，对应滤镜的选项（如 scale 的 w、h 参数） */
    params: Record<string, any>;
    /** 节点在画布上的 X 坐标（前端展示用） */
    x: number;
    /** 节点在画布上的 Y 坐标（前端展示用） */
    y: number;
    /** 入口连接线引用（内部使用） */
    prevs?: FilterLine[];
    /** 出口连接线引用（内部使用） */
    nexts?: FilterLine[];
    /** 关联的滤镜详情引用（内部使用） */
    detail?: FFmpegFilterDetail;
}

/**
 * 滤镜图连线
 * 表示 filter_complex 中滤镜节点之间的连接关系
 *
 * 示例 ffmpeg 命令：
 * ffmpeg -filter_complex "[0:v]scale=1920:1080[v0];[v0][1:v]overlay[outv]"
 * 其中 [0:v]、[v0]、[1:v]、[outv] 等方括号内的标签即为连线的 name
 */
export interface FilterLine {
    /** 连线标签名，对应 filter_complex 中方括号内的标识符
     *  - 从输入节点出来：格式为 "输入编号:流类型:流编号"（如 0:v:0）
     *  - 从滤镜节点出来：为 ffmpeg 生成的随机名或用户定义名
     */
    name: string;
    /** 上游节点 ID */
    prevNodeId: number;
    /** 上游节点输出端口索引 */
    prevNodePortIndex: number;
    /** 下游节点 ID */
    nextNodeId: number;
    /** 下游节点输入端口索引 */
    nextNodePortIndex: number;
    // 对于普通滤镜的输出结果，name 是唯一的；只有对于输入节点的输出结果可以用 输入编号:流类型:流编号 反复使用。而对于媒体输入的输出节点，或者媒体输出的输出节点，并不需要关心 index，因为次序是没影响的
    /** 上游端口坐标（前端展示用） */
    prevXY?: [number, number];
    /** 下游端口坐标（前端展示用） */
    nextXY?: [number, number];
    /** 流类型：V=视频，A=音频，N=无（断开），U=未知（前端展示用） */
    type?: 'V' | 'A' | 'N' | 'U';
    /** 正在创建中的线段的端口方向（前端展示用） */
    invisiblePort?: 'prev' | 'next';
}

/**
 * 输出参数配置
 * 对应一个完整的 ffmpeg 命令的输出部分
 *
 * ffmpeg 支持多个输出文件，每个输出可独立配置视频、音频、容器参数
 * 示例 ffmpeg 命令：
 * ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -c:a aac output.mp4
 */
export interface OutputParams {
    /** 输入参数，对应 ffmpeg 的输入选项（-i、-ss、-f 等） */
    input: OutputParams_input;
    /** 滤镜图配置，对应 ffmpeg 的 -filter_complex 参数 */
    filter: OutputParams_filter;
    /** 输出文件列表，每个元素对应 ffmpeg 命令末尾的一个输出文件
     *  ffmpeg 支持多输出：ffmpeg -i input.mp4 -c:v libx264 out1.mp4 -c:v libvpx out2.webm
     */
    outputs: {
        video: OutputParams_video;
        audio: OutputParams_audio;
        mux: OutputParams_mux;
    }[];
    /** 无具体作用 */
    extra: OutputParams_extra;
}

/** 输入参数配置 */
export type OutputParams_input = {
    /** 输入文件列表，每个元素对应一个 -i 参数 */
    files: InputFile[];
};

/** 滤镜图配置，对应 -filter_complex 参数 */
export type OutputParams_filter = {
    /** 滤镜节点列表 */
    nodes: FilterNode[];
    /** 滤镜连线列表 */
    lines: FilterLine[];
};

/**
 * 视频编码参数
 * 对应 ffmpeg 的视频编码选项
 */
export type OutputParams_video = {
    /** 视频编码器，对应 -c:v 或 -vcodec（如 libx264、libvpx-vp9）。若需 -vn，设置为 "禁用" */
    vcodec: string;
    /** 分辨率，对应 -s 参数（如 1920x1080）或 -vf scale 滤镜 */
    resolution?: string;
    /** 帧率，对应 -r 参数（如 30、60） */
    framerate?: string;
    /** 码率控制模式：可选 CRF、CQP、CBR、ABR、VBR、VBR_HQ、Q。与 ffmpeg 中的编码器设定并不严格对应，FFBox 会自动补充部分参数，如 max_rate 等
     *  - 对于 CRF、CQP、VBR，ratevalue 与实际值是相反的关系。比如编码器的 crf 最大值是 51，用户想要 18，那么 ratevalue 应为 51 - 18 = 33。
     *  - 对于 CBR、ABR，ratevalue 代表 62.5kbps * (2 ^ n)。比如，0 代表 62.5kbps，1 代表 125kbps，2 代表 250kbps，以此类推。
     *  - 对于 Q，ratevalue 与传给 ffmpeg 的参数是相同的。
     */
    ratecontrol?: string;
    ratevalue?: number | string;
    /** 编码器详细设置，对应编码器的私有选项（如 -x264-params） */
    detail: Record<string, any>;
    /** 自定义视频参数，原样附加到 ffmpeg 命令中 */
    custom?: string;
}

/**
 * 音频编码参数
 * 对应 ffmpeg 的音频编码选项
 */
export type OutputParams_audio = {
    /** 音频编码器，对应 -c:a 或 -acodec（如 aac、libmp3lame）。若需 -an，设置为 "禁用" */
    acodec: string;
    /** 码率控制模式，可选 Q、CBR_ABR。与 ffmpeg 中的编码器设定并不严格对应，FFBox 会自动补充部分参数
     *  - 对于 Q，ratevalue 与传给 ffmpeg 的参数是相同的。
     *  - 对于 CBR_ABR，ratevalue 代表 8kbps * (2 ^ n)。比如，0 代表 8kbps，1 代表 16kbps，2 代表 32kbps，以此类推。
     */
    ratecontrol?: string;
    ratevalue?: number | string;
    /** vol 为旧版参数，不建议使用 */
    vol?: number;
    /** 编码器详细设置 */
    detail: Record<string, any>;
    /** 自定义音频参数，原样附加到 ffmpeg 命令中 */
    custom?: string;
};

/**
 * 容器/复用器参数
 * 对应 ffmpeg 的输出容器格式选项
 */
export type OutputParams_mux = {
    /** 容器格式，对应 -f 参数（如 mp4、matroska、flv） */
    format: string;
    /** 是否启用 movflags（MP4 优化选项），对应 -movflags +faststart 等 */
    moveflags: boolean;
    /** 输出文件路径，ffmpeg 命令末尾的输出文件名。默认值为 [filedir]/[filename]_converted.[fileext]，FFBox 会自动替换 [filedir]、[filename]、[fileext] */
    filePath: string;
    /** 输出起始时间（输出端裁剪），对应输出侧的 -ss 参数 */
    begin?: string;
    /** 输出结束时间（输出端裁剪），对应输出侧的 -to 或 -t 参数 */
    end?: string;
    /** 容器/复用器的详细设置，对应 -muxer_options */
    detail: Record<string, any>;
    /** 元数据保留方式，对应 -map_metadata 参数
     *  - false: 不保留
     *  - 'map': 使用 -map_metadata 0
     *  - 'movflags': 使用 movflags 保留
     *  - 'both': 同时使用两种方式
     */
    keepMetadata?: false | 'map' | 'movflags' | 'both';
    /** 文件时间保留方式
     *  - origianl: 保留原始时间
     *  - autoShift: 复制修正后的文件时间（依创建时间）。输出文件的创建时间、修改时间将以创建时间为基准，按照剪裁位置自动调整后进行修改
     *  - fixCTbyMTandShift: 复制修正后的文件时间（依修改时间）。输出文件的创建时间、修改时间将以修改时间为基准，按照剪裁位置自动调整后进行修改，用于修复拷贝后创建时间丢失的问题
     *  - fixByFilenameAndShift: 根据文件名修正新文件时间。用于修复文件时间丢失的问题，将通过文件名作为创建时间，根据剪裁位置自动调整后进行修改
     */
    keepFileTime?: false | 'original' | 'autoShift' | 'fixCTbyMTandShift' | 'fixByFilenameAndShift';
    /** 自定义容器参数，原样附加到 ffmpeg 命令中 */
    custom?: string;
};

/** 额外参数配置 */
export type OutputParams_extra = {
    /** 预设名称，用于保存/加载配置 */
    presetName?: string;
}
```

## Webhook 事件系统

### 事件类型

#### 任务事件
- `task.created`: 任务创建
- `task.started`: 任务开始  
- `task.paused`: 任务暂停
- `task.resumed`: 任务继续
- `task.completed`: 任务完成
- `task.error`: 任务出错
- `task.deleted`: 任务删除
- `task.progress`: 任务进度更新

#### 队列事件
- `queue.started`: 队列启动
- `queue.paused`: 队列暂停

#### 任务列表事件
- `tasklist.changed`: 任务列表变化
- `tasklist.added`: 任务添加
- `tasklist.removed`: 任务删除

#### 通知事件
- `notification`: 通知消息

### Webhook 请求格式

**请求头**:
- `Content-Type: application/json`
- `X-FFBox-Event: {event_type}`
- `X-FFBox-Delivery: {uuid}`
- `X-FFBox-Signature: sha256={hex_digest}` (如果配置了 secret)

**请求体**:
```json
{
  "name": "string",
  "url": "string",
  // secret 是可选的
  "secret": "string",
  "events": [
    "task.created",
    "queue.started",
    "tasklist.changed",
    "string"
  ],
  // filter 是可选的
  "filter": {
    "task_id": [
      0
    ]
  },
  "enabled": true
}
```

### 签名验证 (Node.js 示例)
```javascript
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  return `sha256=${expected}` === signature;
}
```

### 重试机制
- **最大重试次数**: 3 次
- **连续失败 3 次后自动禁用 Webhook**

## 使用示例

### 创建任务示例
```http
POST /api/v1/tasks
Authorization: Bearer <sessionId>
Content-Type: application/json

{
  "taskName": "视频转码",
  "outputParams": {
    "input": { 
      "files": [{ 
        "filePath": "/path/to/input.mp4" 
      }] 
    },
    "outputs": [{
      "video": { 
        "vcodec": "libx264", 
        "ratecontrol": "crf", 
        "ratevalue": 23 
      },
      "audio": { 
        "acodec": "aac" 
      },
      "mux": { 
        "format": "mp4", 
        "filePath": "/path/to/output.mp4" 
      }
    }]
  }
}
```

### 创建 Webhook 示例
```bash
curl -X POST http://localhost:33269/api/v1/webhooks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <sessionId>" \
  -d '{
    "name": "我的回调",
    "url": "https://my-server.com/ffbox-callback",
    "secret": "my-secret",
    "events": ["task.completed", "task.error"],
    "filter": {
      "task_id": [1, 2, 3]
    },
    "enabled": true
  }'
```

## 注意事项

1. **远程 vs 本地任务**: 远程任务需要先上传文件，再调用 merge-upload；本地任务直接使用绝对路径
2. **认证要求**: 如果设置了密码，除 login 外的所有 HTTP 操作都需要 Bearer Token

---
*本文档基于 FFBox 5.3-alpha 版本制作*