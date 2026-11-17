---
name: "3d-generator"
description: "AI Generated 3D Models using SOTA APIs such as Tripo/Meshy/TripoSR/etc served on OneKey Agent Gateway by Craftsman Agent, useful for AI Game, Figurine, Stuffed Toy Generation"
env:
  DEEPNLP_ONEKEY_ROUTER_ACCESS:
    required: true
    description: Onekey Gateway Registered API and Usage access key
dependencies:
  node: []
  python: []
---

# 3d-generator Skills from craftsman-agent 
The Workflow of typical 3D Model Generation is like below. This 3D generation APIs served on OneKey Gateway
include the vendors from "TripoAI", "Meshy" APIs and used on Craftsman Agent 3D/IP/Toy Designer Agent website consoles (https://craftsman-agent.aiagenta2z.com/app/3d-generator).

```commandline
[Text/Single Images/Multi View Images Prompt]  ->  [Create Generation Task: Task ID] -> [Poll Task Results Progress using Task ID]
```

| API                      | Description                                                               |
|--------------------------|---------------------------------------------------------------------------|
| 3d_generator_task_create | Create a new 3D Generation Task From user uploaded images or text prompts |
| 3d_generator_task_poll   | Poll Progress of Task Generation                                          |

### 3D Generation API Types

| API TYPE       | Description                                                                           |
|----------------|---------------------------------------------------------------------------------------|
| image_to_model | 3D Reconstruction from user uploaded images and outputs a .obj,.pbr 3d files          |
| text_to_model  | Poll Progress of Task Generation                                                      |
| multiview_to_model | Generate a 3D model assets using front, left, right, back views of the same character |


Auto-generated skill for OneKey Agent Gateway registered agent `craftsman-agent/craftsman-agent` based on its `api_list` from registered API metas. Available 
to use in CLIs, Skills, Rest APIs, and more agent preferred formats. The online 3D generator website is https://craftsman-agent.aiagenta2z.com/app/3d-generator.
And you can also find gallery of 3D Generated Digital Assets in https://craftsman-agent.aiagenta2z.com/gallery/3d_generator.

[//]: # (![3D Generated Images]&#40;https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png&#41;)
<img src="https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png" alt="Craftsman-agent Perler Beads for Minecraft Diamond Pickaxes" width="500" />

| Section                       | Description                                   |
|-------------------------------|-----------------------------------------------|
| Craftsman 3D Generator Online | https://craftsman-agent.aiagenta2z.com/app/3d-generator |
| Craftsman Website     | https://craftsman-agent.aiagenta2z.com           |
| Craftsman App         | https://craftsman-agent.aiagenta2z.com/app       |
| Craftsman Gallery     | https://craftsman-agent.aiagenta2z.com/gallery   |
| Craftsman Workspace   | https://craftsman-agent.aiagenta2z.com/workspace |
| Craftsman Marketplace | https://craftsman-agent.aiagenta2z.com/marketplace |


## Quick Start
Set the registered OneKey Gateway access key `DEEPNLP_ONEKEY_ROUTER_ACCESS` from AI Agent Marketplace at the [Website](https://deepnlp.org/workspace/keys).


```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key
```

# 1. Text to Model

## 1.1 Curl Request
#### Task Create API

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "3d_generator_task_create",
  "data": {
    "prompt": "Generate A Figurine of Steve in Minecraft",
    "images": [],
    "provider_model_id": "tripo/tripo",
    "session_name": "3D Build Plan",
    "tag_list": "",
    "mode": "basic"
  }
}'
```

##### Input Parameters Definition
| Parameters        | Description                      |
|-------------------|----------------------------------|
| prompt            | Text Prompt                      |
| images            | Array of image URLs              |
| provider_model_id | options: tripo/tripo,meshy/meshy |
| mode              | basic/standard/advanced/demo     |


#### Expected Outputs

```json
{
  "provider_model_id": "tripo/tripo",
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "session_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "title": "3D Build Plan",
  "workspace_session_id": "",
  "tag_list": "",
  "final_image_url": "",
  "status": "running"
}
```

##### Outputs Parameters Definition
| Parameters | Description                                                                                                                                        |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| provider_model_id   | The 3D Generator provider id, such as "tripo/tripo", "meshy/meshy",                                                                                |
| task_id    | The Task ID of created 3d generator Task                                                                                                           |
| session_id | The generated workspace session ID, you can view your session on workspace at https://craftsman-agent.aiagenta2z.com/workspace for logged in user. |
| status     | running,completed,etc                                                                                                                              |


#### Task Poll API

##### Input Parameters Definition
| Parameters   | Description                |
|--------------|----------------------------|
| data.task_id | The task id to poll status |
| data.kwargs  | Other optional parameters  |


#### Input Request
```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "3d_generator_task_poll",
  "data": {
    "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
    "kwargs": {
      "provider_model_id": "tripo/tripo",
      "mode": "basic"
    }
  }
}'
```


##### Outputs Parameters Definition

| Parameters        | Description                                        |
|-------------------|----------------------------------------------------|
| task_id           | The task id of generated 3d model                  |
| status            | The status of generated task                       |
| progress | 0-100, int, progress of Task                       |
| model             | 3D model downloadable urls                         |
| preview            | The rendering preview of the 3d model              |
| credits            | Credits consumed for each 3D generation Task       |
| raw_output         | The original raw outputs of tripo3d.ai or meshy.ai |


#### Expected Outputs 

```json
{
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "status": "success",
  "progress": 100,
  "model": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb",
    "type": "glb"
  },
  "preview": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/legacy_mesh.webp",
    "type": "webp"
  },
  "metadata": {
    "model_version": "P1-20260311",
    "texture": true,
    "pbr": true,
    "face_limit": null,
    "export_uv": true
  },
  "credits": 50,
  "raw_output": {
    "code": 0,
    "status": "success",
    "data": {
      "type": "multiview_to_model",
      "status": "success",
      "progress": 100,
      "input": {
        "pbr": true,
        "files": [
          {
            "object": {
              "key": "tcli_0bc797f67ec048078fb528e60503c957/20260814/96b2116e-4b86-4d3c-af04-baf0da0c23ac/url_fetch/mv_0.png",
              "bucket": "tripo-data"
            }
          },
          null,
          {
            "object": {
              "key": "tcli_0bc797f67ec048078fb528e60503c957/20260814/96b2116e-4b86-4d3c-af04-baf0da0c23ac/url_fetch/mv_2.png",
              "bucket": "tripo-data"
            }
          },
          {
            "object": {
              "key": "tcli_0bc797f67ec048078fb528e60503c957/20260814/96b2116e-4b86-4d3c-af04-baf0da0c23ac/url_fetch/mv_3.png",
              "bucket": "tripo-data"
            }
          }
        ],
        "texture": true,
        "export_uv": true,
        "model_version": "P1-20260311"
      },
      "output": {
        "model_url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb",
        "rendered_image_url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/legacy_mesh.webp",
        "model_url_original": "https://tripo-data.rg1.data.tripo3d.com/tcli_0bc797f67ec048078fb528e60503c957/20260814/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly90cmlwby1kYXRhLnJnMS5kYXRhLnRyaXBvM2QuY29tL3RjbGlfMGJjNzk3ZjY3ZWMwNDgwNzhmYjUyOGU2MDUwM2M5NTcvMjAyNjA4MTQvOTZiMjExNmUtNGI4Ni00ZDNjLWFmMDQtYmFmMGRhMGMyM2FjL3RyaXBvX3Bicl9tb2RlbF85NmIyMTE2ZS00Yjg2LTRkM2MtYWYwNC1iYWYwZGEwYzIzYWMuZ2xiIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzg2Nzc3MzI1fX19XX0_&Signature=N9WpKJRtdSBN36~6QuF2ujoONVnZARvHaZ5Mx5urx1WdYcgUGZ4QV9uhIFyEEt~Kbx6k6ATIlA08nD7pV76ELabEyvhtq6AUUxmTSyf-EtdDJdfCFB~7L8LufrXlHrBw29sEtr5jFzJc7qnqw556Y-0FlTgOXDk0V-t5DJJOIvIy31kvMuYQ3TiXY8uw6DIurKlTfy4BzPqgRcn6oHXlqOs2NMyoINKw2B62MzMLqUlf4w8k5rPOkl8twLGk0hbt93MMVpjZ24NgcBSck8Y4~JWIjitEPmb1swhnOSNMiUEIKQkffcG1xIKuEYcQshdEDpQRq1aUh6KxzplfuyN-iw__&Key-Pair-Id=K1676C64NMVM2J",
        "rendered_image_url_original": "https://tripo-data.rg1.data.tripo3d.com/tcli_0bc797f67ec048078fb528e60503c957/20260814/96b2116e-4b86-4d3c-af04-baf0da0c23ac/legacy_mesh.webp?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly90cmlwby1kYXRhLnJnMS5kYXRhLnRyaXBvM2QuY29tL3RjbGlfMGJjNzk3ZjY3ZWMwNDgwNzhmYjUyOGU2MDUwM2M5NTcvMjAyNjA4MTQvOTZiMjExNmUtNGI4Ni00ZDNjLWFmMDQtYmFmMGRhMGMyM2FjL2xlZ2FjeV9tZXNoLndlYnAiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3ODY3NzczMjV9fX1dfQ__&Signature=Xy4anDZvmQX8Oe6z9TuPAqtTZYs1zTpXN7a2Ex2M5UTg-nYxVnCPze82cChCP9joJWg8IbdiRMTBEYy3aFT6uxPu~XzrxF2~m8mRQhsTwkm0WETlGcVSTeSfNiCXXCmZPsfA~UT5~tURgKeiXuh9XuLK100vakVbxxkAxwK0EG4KS8u-CwsMLYBwyml9Th-AIeCegr9WHNAnrMX9L5uIDdF0mcRDJO7aOc9caUEvFQGgG0K9zCuWbiCCqh2IcirEXp0PBvMwYXwjR2-pKqWjWQ-TFeGlZeKYadVaOX45V5jDn1mkMjSQt3kJbrXYY6WBbUPk0n9gCTQoidpWCt2Dyw__&Key-Pair-Id=K1676C64NMVM2J"
      },
      "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
      "created_at": "2026-08-14T06:59:54.087075Z",
      "completed_at": "2026-08-14T07:01:13.058416Z",
      "credits_consumed": 50
    }
  },
  "session_id": "",
  "title": "",
  "workspace_session_id": "",
  "tag_list": ""
}
```


## 1.2 CLIs Usage

```bash
npx onekey agent craftsman-agent/craftsman-agent 3d_generator_task_create '{"prompt": "Generate A Figurine of Steve in Minecraft", "images": [], "provider_model_id": "tripo/tripo", "session_name": "3D Build Plan", "tag_list": "", "mode": "basic"}'

npx onekey agent craftsman-agent/craftsman-agent 3d_generator_task_poll '{"task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac", "kwargs": {"provider_model_id": "tripo/tripo", "mode": "basic"}}'
```

# 2. Image to Model

## 2.1 Curl Request
#### a. Task Create API Demo


#### Input Parameters Definition

| Parameters        | Description                      |
|-------------------|----------------------------------|
| prompt            | Text Prompt                      |
| images            | Array of image URLs              |
| provider_model_id | options: tripo/tripo,meshy/meshy |
| mode              | basic/standard/advanced/demo     |

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "3d_generator_task_create",
  "data": {
    "prompt": "",
    "images": ["https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png"],
    "provider_model_id": "tripo/tripo",
    "session_name": "3D Build Plan",
    "tag_list": "",
    "mode": "basic"
  }
}'
```

#### Input Parameters Definition

| Parameters        | Description                 |
|-------------------|-----------------------------|
| provider_model_id | The provider model id       |
| task_id           | The task if for polling...  |

#### Expected Outputs
```json
{"provider_model_id":"tripo/tripo","task_id":"96b2116e-4b86-4d3c-af04-baf0da0c23ac","session_id":"96b2116e-4b86-4d3c-af04-baf0da0c23ac","title":"3D Build Plan","workspace_session_id":"","tag_list":"","final_image_url":"https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png","status":"running"}
```

#### b. Task Poll API

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "3d_generator_task_poll",
  "data": {
    "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
    "kwargs": {
      "provider_model_id": "tripo/tripo",
      "mode": "basic"
    }
  }
}'
```

#### Input Parameters Definition

| Parameters | Description |
|------------|----------|
| task_id | The ID of the task generated from task create API |
| kwargs | Extra parameters like provider_model_id and mode |

#### Expected Outputs

```json
{
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "status": "success",
  "progress": 100,
  "model": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb",
    "type": "glb"
  },
  "preview": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/legacy_mesh.webp",
    "type": "webp"
  },
  "metadata": {
    "model_version": "P1-20260311",
    "texture": true,
    "pbr": true,
    "face_limit": null,
    "export_uv": true
  },
  "credits": 50
}
```

## 2.2 CLIs Usage

```bash
npx onekey agent craftsman-agent/craftsman-agent 3d_generator_task_create '{"prompt": "", "images": ["https://us-static.aiagenta2z.com/local/files-wd/onekey_llm_router/7485ee2a-ae58-48e3-9dc8-eaf1d3d1c4a7.png"], "provider_model_id": "tripo/tripo", "session_name": "3D Build Plan", "tag_list": "", "mode": "basic"}'

npx onekey agent craftsman-agent/craftsman-agent 3d_generator_task_poll '{"task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac", "kwargs": {"provider_model_id": "tripo/tripo", "mode": "basic"}}'
```

# 3. MultiView to Model
## 3.1 Curl Request
#### Inputs Parameters Definition

| Parameters        | Description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| prompt            | Text Prompt                                                                                   |
| images            | Array of image URLs                                                                           |
| multi_view        | The multi_view is a dict of front,left(optional),right,back images urls for 3D reconstruction |
| provider_model_id | options: tripo/tripo,meshy/meshy                                                              |
| mode              | basic/standard/advanced/demo                                                                  |

#### Task Create API

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "3d_generator_task_create",
  "data": {
    "prompt": "",
    "images": ["https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png"],
    "multi_view": {
        "front": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_front.png",
        "right": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_right.png",
        "back": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_back.png"
    },
    "provider_model_id": "tripo/tripo",
    "session_name": "3D Build Plan",
    "tag_list": "",
    "mode": "basic"
  }
}'
```

#### Expected Outputs

```json
{"provider_model_id":"tripo/tripo","task_id":"96b2116e-4b86-4d3c-af04-baf0da0c23ac","session_id":"96b2116e-4b86-4d3c-af04-baf0da0c23ac","title":"3D Build Plan","workspace_session_id":"","tag_list":"","final_image_url":"https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png","status":"running"}
```

#### Task Poll API

```bash
export DEEPNLP_ONEKEY_ROUTER_ACCESS=your_access_key

curl -X POST "https://agent.deepnlp.org/agent_router" \
-H "Content-Type: application/json" \
-H "X-OneKey: $DEEPNLP_ONEKEY_ROUTER_ACCESS" \
-d '{
  "unique_id": "craftsman-agent/craftsman-agent",
  "api_id": "3d_generator_task_poll",
  "data": {
    "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
    "kwargs": {
      "provider_model_id": "tripo/tripo",
      "mode": "basic"
    }
  }
}'
```

#### Expected Outputs

```json
{
  "task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac",
  "status": "success",
  "progress": 100,
  "model": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/tripo_pbr_model_96b2116e-4b86-4d3c-af04-baf0da0c23ac.glb",
    "type": "glb"
  },
  "preview": {
    "url": "https://us-static.aiagenta2z.com/container/aiagenta2z/3d_generator/static/96b2116e-4b86-4d3c-af04-baf0da0c23ac/legacy_mesh.webp",
    "type": "webp"
  }
}
```

## 3.2 CLIs Usage

```bash
npx onekey agent craftsman-agent/craftsman-agent 3d_generator_task_create '{"prompt": "", "images": ["https://static.aiagenta2z.com/container/craftsman-agent/default/static/derekzz/a49f905b-4e0d-40c6-af7a-c37be3d1741e/3ccb042bbd9b41c3a9f5d31c564ef4c0.png"], "multi_view": {"front": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_front.png", "right": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_right.png", "back": "https://craftsman-agent.aiagenta2z.com/static/derekzz/75302fb3-b0f4-4bfe-a406-1c97eda64dbf/build_back.png"}, "provider_model_id": "tripo/tripo", "session_name": "3D Build Plan", "tag_list": "", "mode": "basic"}'

npx onekey agent craftsman-agent/craftsman-agent 3d_generator_task_poll '{"task_id": "96b2116e-4b86-4d3c-af04-baf0da0c23ac", "kwargs": {"provider_model_id": "tripo/tripo", "mode": "basic"}}'
```
