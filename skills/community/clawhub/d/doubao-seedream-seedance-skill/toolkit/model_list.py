from typing import Any, Dict, List


class ModelList:
    def list_image_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "doubao-seedream-4-0-250828",
                "name": "Seedream 4.0",
                "type": "image_generation",
                "description": "High-quality text-to-image model",
            },
            {
                "id": "doubao-seedream-4-5-251128",
                "name": "Seedream 4.5",
                "type": "image_generation",
                "description": "Latest-generation text-to-image model",
            },
        ]

    def list_video_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "doubao-seedance-1-5-pro-251215",
                "name": "Seedance 1.5 Pro",
                "type": "video_generation",
                "description": "High-quality video generation model",
            },
            {
                "id": "doubao-seedance-1-5-250415",
                "name": "Seedance 1.5",
                "type": "video_generation",
                "description": "Standard video generation model",
            },
        ]

    def list_vision_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "doubao-seed-1-6-vision-250815",
                "name": "Seed Vision 1.6",
                "type": "vision_understanding",
                "description": "Multimodal vision understanding model",
            }
        ]

    def get_all_models(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "image_generation": self.list_image_models(),
            "video_generation": self.list_video_models(),
            "vision_understanding": self.list_vision_models(),
        }

    def list_expandable_ark_services(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "Text Embedding",
                "endpoint": "/embeddings/text",
                "auth": "Bearer API Key",
            },
            {
                "name": "Knowledge Base Search",
                "endpoint": "/knowledge/search",
                "auth": "Bearer API Key",
            },
            {
                "name": "Knowledge Base Chat",
                "endpoint": "/knowledge/chat",
                "auth": "Bearer API Key",
            },
            {
                "name": "3D Generation",
                "endpoint": "/3d/generations/tasks",
                "auth": "Bearer API Key",
            },
            {
                "name": "Web Search Tool",
                "endpoint": "/tools/web_search",
                "auth": "Bearer API Key",
            },
            {
                "name": "Context Cache",
                "endpoint": "/context/cache",
                "auth": "Bearer API Key",
            },
            {
                "name": "File Upload",
                "endpoint": "/files/upload",
                "auth": "Bearer API Key",
            },
            {
                "name": "File Query",
                "endpoint": "/files/{file_id}",
                "auth": "Bearer API Key",
            },
        ]
