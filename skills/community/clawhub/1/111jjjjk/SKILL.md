1. 首先要确认，图片、文件是保存多久. 跟聊天记录的时长是否一致。

2. 
spring.application.name.llm-playground-service


imagePaths 使用这个参数接图片
imagePath 单张
imagePaths 多张


filePaths 使用这个参数接文件
filePath 单个文件
filePaths 多个文件


本地调试 需要在header 中添加 currentuser 参数

http://10.73.171.38:30110/largemodel/llmstudio/fs/uploadImg 上传图片地址
http://10.73.171.38:30110/largemodel/llmstudio/fs/6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763357942287_CGM.png 显示地址
6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763357942287_CGM.png 返回内容

http://10.73.171.38:30110/largemodel/llmstudio/fs/6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763360443721_1763360443713_493caaf73fcc20446dc764987a53fad9.jpg
6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763360443721_1763360443713_493caaf73fcc20446dc764987a53fad9.jpg




http://10.73.171.38:30110/largemodel/llmstudio/fs/uploadFile 上传文件地址
文件没有显示
6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/error.txt 返回内容
















工作流

    文件上传：http://188.103.147.179:30181/largemodel/llmstudio/llm-workflow-service/api/v1/workflow/sign_file_url

{
    "id": "6915755ec2e807195c7a8e6b",
    "input": {
        "BOT_USER_INPUT": "yyyyy",
        "BOT_CHAT_HISTORY": null,
        "BOT_USER_FILE": "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763015301444_CGM.png"
    },
    "lastUpdate": "1763015276963",
    "canvasType": "DRAFT"
} 
--- "reason": "illegal input， offset 1, char 由",

{
    "browserEnable": true,
    "imagePath": null,
    "imagePaths": [
        "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763030284427_10.30加班打卡记录.jpg",
        "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763030292138_11.04加班打卡记录.jpg"
    ],
    "filePaths": [
        "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/2025.11.13-2025.11.21.txt",
        "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/2025.11.13-2025.11.21.txt",
        "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/上下班打卡_日报_20250720-20250920-30天.csv"
    ],
    "filePath": "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/2025.11.13-2025.11.21.txt",
    "recordId": "1762860012769ojonrbvlw",
    "video": {
        "videoImagePath": null,
        "videoPath": null,
        "duration": null
    },
    "docId": null,
    "sourceDoc": {
        "type": 0,
        "list": [
            {
                "name": "2025.11.13-2025.11.21.txt",
                "size": 6567,
                "status": "success",
                "path": "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/2025.11.13-2025.11.21.txt",
                "showRef": false
            },
            {
                "name": "2025.11.13-2025.11.21.txt",
                "size": 6567,
                "status": "success",
                "path": "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/2025.11.13-2025.11.21.txt",
                "showRef": false
            },
            {
                "name": "上下班打卡_日报_20250720-20250920-30天.csv",
                "size": 27923,
                "status": "success",
                "path": "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/上下班打卡_日报_20250720-20250920-30天.csv",
                "showRef": false
            }
        ]
    },
    "params": {},
    "modelId": "jiutian-lan",
    "input": "用文件内容吹牛逼",
    "sourceType": "app",
    "agentApp": {
        "appId": "690d98e00b367959f1fcc8dd",
        "appName": "cgm_test",
        "debug": true,
        "id": "690d98e00b367959f1fcc8dd",
        "name": "cgm_test",
        "avatar": "public/avatar/1762498777498_1762498777496_1762498777487_text2Image.jpg",
        "desc": "cgm_test",
        "prolog": null,
        "userId": "6e35a560-0530-4b72-8b1c-672f9bb5d531",
        "username": "cxy_test",
        "createTime": "2025-11-07 14:59:44",
        "updateTime": "2025-11-13 18:37:49",
        "modelId": "jiutian-lan",
        "params": {},
        "prompt": "",
        "example": [
            {
                "question": "帮忙吹牛逼",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            },
            {
                "question": "",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            }
        ],
        "plugList": [],
        "mcpList": null,
        "workflowList": [
            {
                "id": "690db390713cfa3eba14f836",
                "canvasType": "PRIVATE_RELEASE"
            }
        ],
        "showRefer": 0,
        "memory": 0,
        "userVisibleMemory": false,
        "showSuggestInput": 1,
        "bot_voice": null,
        "klFile": null,
        "klBases": [],
        "clickCount": 0,
        "appType": 6,
        "status": 0,
        "pubTime": null,
        "rejectReason": null,
        "offLineReason": null,
        "favoriteCount": null,
        "isRecommended": null,
        "recommendTime": null,
        "chatCount": 0,
        "topN": 3,
        "threshold": 0.65,
        "addContext": null,
        "rerank": 1,
        "rerankModel": "BAAI/bge-reranker-large",
        "searchType": 0,
        "answerModelId": "qwen3-32b",
        "temperature": 0.8,
        "topP": 0.5,
        "kbSearchModel": "forced",
        "chatMode": "workflow",
        "planModel": null,
        "cards": null,
        "mobileCertify": null,
        "goodCount": 0,
        "badCount": 0,
        "teamId": null,
        "coopUids": null,
        "coopUserInfo": null,
        "lastUpdateTime": null,
        "coopRole": "creater",
        "publishedTemplate": null,
        "agentCardId": null,
        "questionList": [
            {
                "question": "帮忙吹牛逼",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            },
            {
                "question": "",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            }
        ]
    }
}



LLM
    图片上传：http://188.103.147.179:30181/largemodel/llmstudio/fs/uploadImg
    文件上传：http://188.103.147.179:30181/largemodel/llmstudio/fs/uploadFile
    csv上传：http://188.103.147.179:30181/largemodel/llmstudio/fs/uploadFile

请求参数
{
    "browserEnable": true,
    "imagePath": null,
    "filePath": null,
    "recordId": "1763016007604y5aej1it3",
    "video": {
        "videoImagePath": null,
        "videoPath": null,
        "duration": null
    },
    "docId": null,
    "sourceDoc": {
        "type": 0,
        "list": []
    },
    "params": {},
    "modelId": "jiutian-lan",
    "input": "123445",
    "name": "2323",
    "sourceType": "app",
    "agentApp": {
        "appId": "69157c599ddc670712531443",
        "appName": "cgm_test",
        "debug": true,
        "id": "69157c599ddc670712531443",
        "name": "cgm_test",
        "avatar": "public/avatar/1763015767084_CGM.png",
        "desc": "cgm_test",
        "prolog": null,
        "userId": "6e35a560-0530-4b72-8b1c-672f9bb5d531",
        "username": "cxy_test",
        "createTime": "2025-11-13 14:36:09",
        "updateTime": "2025-11-13 14:36:09",
        "modelId": "jiutian-lan",
        "params": {},
        "prompt": "使用输入参数进行吹牛逼，吹越大越好！",
        "example": [
            {
                "question": "",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            }
        ],
        "plugList": [],
        "mcpList": null,
        "workflowList": [],
        "showRefer": 0,
        "memory": 0,
        "userVisibleMemory": false,
        "showSuggestInput": 1,
        "klFile": null,
        "klBases": [],
        "clickCount": 0,
        "appType": 6,
        "status": 0,
        "pubTime": null,
        "rejectReason": null,
        "offLineReason": null,
        "favoriteCount": null,
        "isRecommended": null,
        "recommendTime": null,
        "chatCount": 0,
        "topN": 3,
        "threshold": 0.65,
        "addContext": null,
        "rerank": 1,
        "rerankModel": "BAAI/bge-reranker-large",
        "searchType": 0,
        "answerModelId": "Qwen3-32B",
        "temperature": 0.84,
        "topP": 0.5,
        "kbSearchModel": "forced",
        "chatMode": "llm",
        "planModel": "Qwen3-32B-fc",
        "cards": {},
        "mobileCertify": 0,
        "goodCount": 0,
        "badCount": 0,
        "teamId": null,
        "coopUids": null,
        "coopUserInfo": null,
        "lastUpdateTime": null,
        "coopRole": "creater",
        "publishedTemplate": null,
        "questionList": [
            {
                "question": "",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            }
        ]
    }
}

请求参数
{
    "browserEnable": true,
    "imagePath": "6e35a560-0530-4b72-8b1c-672f9bb5d531/upload/1763016377381_CGM.png",
    "filePath": null,
    "recordId": "1763016347001xgjj90sl4",
    "video": {
        "videoImagePath": null,
        "videoPath": null,
        "duration": null
    },
    "docId": null,
    "sourceDoc": {
        "type": 0,
        "list": []
    },
    "params": {},
    "modelId": "jiutian-lan",
    "input": "用图片内容",
    "name": "用图片内容",
    "sourceType": "app",
    "agentApp": {
        "appId": "69157c599ddc670712531443",
        "appName": "cgm_test",
        "debug": true,
        "id": "69157c599ddc670712531443",
        "name": "cgm_test",
        "avatar": "public/avatar/1763015767084_CGM.png",
        "desc": "cgm_test",
        "prolog": null,
        "userId": "6e35a560-0530-4b72-8b1c-672f9bb5d531",
        "username": "cxy_test",
        "createTime": "2025-11-13 14:36:09",
        "updateTime": "2025-11-13 14:36:09",
        "modelId": "jiutian-lan",
        "params": {},
        "prompt": "",
        "example": [
            {
                "question": "",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            }
        ],
        "plugList": [],
        "mcpList": null,
        "workflowList": [],
        "showRefer": 0,
        "memory": 0,
        "userVisibleMemory": false,
        "showSuggestInput": 1,
        "klFile": null,
        "klBases": [],
        "clickCount": 0,
        "appType": 6,
        "status": 0,
        "pubTime": null,
        "rejectReason": null,
        "offLineReason": null,
        "favoriteCount": null,
        "isRecommended": null,
        "recommendTime": null,
        "chatCount": 0,
        "topN": 3,
        "threshold": 0.65,
        "addContext": null,
        "rerank": 1,
        "rerankModel": "BAAI/bge-reranker-large",
        "searchType": 0,
        "answerModelId": "Jiutian-75B",
        "temperature": 0.9,
        "topP": 0.5,
        "kbSearchModel": "forced",
        "chatMode": "llm",
        "planModel": "jiutian_75b_fc",
        "cards": {},
        "mobileCertify": 0,
        "goodCount": 0,
        "badCount": 0,
        "teamId": null,
        "coopUids": null,
        "coopUserInfo": null,
        "lastUpdateTime": null,
        "coopRole": "creater",
        "publishedTemplate": null,
        "questionList": [
            {
                "question": "",
                "file": {
                    "path": "",
                    "name": "",
                    "type": "",
                    "size": 0,
                    "status": "",
                    "message": ""
                }
            }
        ]
    }
}