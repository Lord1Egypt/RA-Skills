#!/usr/bin/env python3
"""
ComfyUI Automation Skill

This script automates the execution of ComfyUI workflows using the RunningHub API.
It follows these steps:
1. Receive workflow identifier from user
2. Collect necessary materials based on workflow requirements
3. Request user confirmation before execution
4. Execute workflow using ComfyUI Task 1 - Simple API
5. Monitor execution status and return results
"""

import requests
import time
import json
import os
from urllib.parse import urlparse

class ComfyUIAutomation:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.runninghub.cn/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def upload_file(self, file_path):
        """Upload a file to RunningHub and return the filename"""
        try:
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                return None
            
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            print(f"Uploading file: {filename} ({file_size} bytes)")
            
            upload_url = f"{self.base_url}/upload"
            
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'application/octet-stream')}
                upload_headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                response = requests.post(
                    upload_url,
                    headers=upload_headers,
                    files=files
                )
            
            if response.status_code == 200:
                result = response.json()
                uploaded_filename = result.get('filename', filename)
                print(f"File uploaded successfully: {uploaded_filename}")
                return uploaded_filename
            else:
                print(f"Error uploading file: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
    
    def is_url(self, string):
        """Check if a string is a valid URL"""
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    def get_workflow_json(self, workflow_id):
        """Get workflow JSON from RunningHub"""
        try:
            response = requests.get(
                f"{self.base_url}/workflow/{workflow_id}/json",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting workflow JSON: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error getting workflow JSON: {e}")
            return None
    
    def analyze_workflow_inputs(self, workflow_json):
        """Analyze workflow to find all modifiable inputs"""
        required_inputs = []
        
        if not workflow_json:
            return required_inputs
        
        for node_id, node_data in workflow_json.items():
            class_type = node_data.get('class_type', '')
            inputs = node_data.get('inputs', {})
            meta = node_data.get('_meta', {})
            title = meta.get('title', class_type)
            
            node_inputs = []
            
            if class_type == 'LoadImage':
                node_inputs.append({
                    'key': 'image',
                    'type': 'image',
                    'title': 'Image',
                    'current_value': inputs.get('image', '')
                })
            elif class_type in ['CLIPTextEncode', 'CLIPTextEncode (NSP)']:
                node_inputs.append({
                    'key': 'text',
                    'type': 'text',
                    'title': 'Text',
                    'current_value': inputs.get('text', '')
                })
            elif class_type == 'Seed (rgthree)':
                node_inputs.append({
                    'key': 'seed',
                    'type': 'number',
                    'title': 'Seed',
                    'current_value': inputs.get('seed', 0)
                })
            elif class_type == 'RH_Translator':
                node_inputs.append({
                    'key': 'prompt',
                    'type': 'text',
                    'title': 'Prompt',
                    'current_value': inputs.get('prompt', '')
                })
            elif class_type == 'KSampler':
                if 'seed' in inputs and not isinstance(inputs['seed'], list):
                    node_inputs.append({
                        'key': 'seed',
                        'type': 'number',
                        'title': 'Seed',
                        'current_value': inputs.get('seed', 0)
                    })
                if 'steps' in inputs and not isinstance(inputs['steps'], list):
                    node_inputs.append({
                        'key': 'steps',
                        'type': 'number',
                        'title': 'Steps',
                        'current_value': inputs.get('steps', 20)
                    })
                if 'cfg' in inputs and not isinstance(inputs['cfg'], list):
                    node_inputs.append({
                        'key': 'cfg',
                        'type': 'number',
                        'title': 'CFG',
                        'current_value': inputs.get('cfg', 7.0)
                    })
                if 'denoise' in inputs and not isinstance(inputs['denoise'], list):
                    node_inputs.append({
                        'key': 'denoise',
                        'type': 'number',
                        'title': 'Denoise',
                        'current_value': inputs.get('denoise', 1.0)
                    })
            elif class_type == 'easy sam3ImageSegmentation':
                if 'threshold' in inputs and not isinstance(inputs['threshold'], list):
                    node_inputs.append({
                        'key': 'threshold',
                        'type': 'number',
                        'title': 'Threshold',
                        'current_value': inputs.get('threshold', 0.4)
                    })
            elif class_type == 'ControlNetInpaintingAliMamaApply':
                if 'strength' in inputs and not isinstance(inputs['strength'], list):
                    node_inputs.append({
                        'key': 'strength',
                        'type': 'number',
                        'title': 'Strength',
                        'current_value': inputs.get('strength', 1.0)
                    })
            elif class_type == 'ModelSamplingAuraFlow':
                if 'shift' in inputs and not isinstance(inputs['shift'], list):
                    node_inputs.append({
                        'key': 'shift',
                        'type': 'number',
                        'title': 'Shift',
                        'current_value': inputs.get('shift', 3.1)
                    })
            
            if node_inputs:
                required_inputs.append({
                    'node_id': node_id,
                    'class_type': class_type,
                    'title': title,
                    'inputs': node_inputs
                })
        
        return required_inputs
    
    def get_workflow_info(self, workflow_identifier):
        """Get workflow information by identifier, or create a new one if not found"""
        try:
            # First try to get by workflowId
            response = requests.get(
                f"{self.base_url}/workflow/{workflow_identifier}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            
            # If not found, try to search by nickname
            response = requests.get(
                f"{self.base_url}/workflow/search",
                headers=self.headers,
                params={"nickname": workflow_identifier}
            )
            if response.status_code == 200:
                results = response.json()
                if results and len(results) > 0:
                    return results[0]
            
            # If workflow not found, ask user if they want to create a new one
            print(f"Workflow with identifier '{workflow_identifier}' not found.")
            create_new = input("Do you want to create a new workflow? (y/n): ")
            
            if create_new.lower() == "y":
                # Create a new workflow
                new_workflow = self.create_new_workflow(workflow_identifier)
                return new_workflow
            else:
                return None
        except Exception as e:
            print(f"Error getting workflow info: {e}")
            # If error occurs, ask user if they want to create a new workflow
            create_new = input("Error getting workflow info. Do you want to create a new workflow? (y/n): ")
            if create_new.lower() == "y":
                new_workflow = self.create_new_workflow(workflow_identifier)
                return new_workflow
            else:
                return None
    
    def create_new_workflow(self, workflow_identifier):
        """Create a new workflow"""
        print("\nCreating a new workflow...")
        
        # Get workflow name with uniqueness check
        existing_workflow_names = ["图像生成", "图像编辑", "视频生成", "音频处理", "多模态合成"]
        
        while True:
            workflow_name = input("Enter a name for the new workflow: ")
            if not workflow_name:
                workflow_name = workflow_identifier
            
            if workflow_name in existing_workflow_names:
                print(f"Error: Workflow name '{workflow_name}' already exists. Please choose a unique name.")
            else:
                break
        
        # Select required materials
        print("\nSelect required materials for the new workflow:")
        print("1. text_prompt (Text prompt)")
        print("2. image_input (Image URL)")
        print("3. video_input (Video URL)")
        print("4. audio_input (Audio URL)")
        print("5. processing_params (Processing parameters)")
        
        required_materials = []
        while True:
            choice = input("\nEnter material type number (0 to finish): ")
            if choice == "0":
                break
            elif choice == "1":
                if "text_prompt" not in required_materials:
                    required_materials.append("text_prompt")
                    print("Added text_prompt to required materials")
            elif choice == "2":
                if "image_input" not in required_materials:
                    required_materials.append("image_input")
                    print("Added image_input to required materials")
            elif choice == "3":
                if "video_input" not in required_materials:
                    required_materials.append("video_input")
                    print("Added video_input to required materials")
            elif choice == "4":
                if "audio_input" not in required_materials:
                    required_materials.append("audio_input")
                    print("Added audio_input to required materials")
            elif choice == "5":
                if "processing_params" not in required_materials:
                    required_materials.append("processing_params")
                    print("Added processing_params to required materials")
            else:
                print("Invalid choice, please try again.")
        
        # Generate a new workflow ID if not provided
        if not workflow_identifier.startswith("wf_"):
            import random
            import string
            workflow_id = "wf_" + ''.join(random.choices(string.digits, k=6))
        else:
            workflow_id = workflow_identifier
        
        # Create workflow info object
        workflow_info = {
            "id": workflow_id,
            "nickname": workflow_name,
            "required_materials": required_materials
        }
        
        print(f"\nNew workflow created:")
        print(f"ID: {workflow_id}")
        print(f"Name: {workflow_name}")
        print(f"Required materials: {', '.join(required_materials)}")
        
        return workflow_info
    
    def collect_materials(self, workflow_info):
        """Collect necessary materials based on workflow requirements"""
        materials = {}
        
        # Workflow material mapping based on workflow ID
        workflow_materials = {
            "wf_123456": ["text_prompt"],  # 图像生成
            "wf_789012": ["text_prompt", "image_input"],  # 图像编辑
            "wf_345678": ["text_prompt", "image_input"],  # 视频生成
            "wf_901234": ["audio_input", "processing_params"],  # 音频处理
            "wf_567890": ["text_prompt", "image_input", "audio_input"]  # 多模态合成
        }
        
        # Get workflow ID
        workflow_id = workflow_info.get("id")
        workflow_name = workflow_info.get("nickname", "Unknown")
        
        print(f"\nCollecting materials for workflow: {workflow_name} (ID: {workflow_id})")
        
        # Determine required materials
        # First check if workflow_info has required_materials field (for newly created workflows)
        required_materials = workflow_info.get("required_materials", [])
        
        # If not, try to get from workflow_materials mapping
        if not required_materials:
            required_materials = workflow_materials.get(workflow_id, [])
        
        # If still no materials, try to detect from workflow info
        if not required_materials:
            # Analyze workflow to determine required materials
            # This is a simplified version - in a real implementation, you would
            # parse the workflow JSON to determine exactly what materials are needed
            
            # Example: Check for common material types
            if "text_prompt" in str(workflow_info):
                required_materials.append("text_prompt")
            
            if "image_input" in str(workflow_info):
                required_materials.append("image_input")
            
            if "video_input" in str(workflow_info):
                required_materials.append("video_input")
            
            if "audio_input" in str(workflow_info):
                required_materials.append("audio_input")
        
        # Collect required materials with validation
        if required_materials:
            print(f"\nThis workflow requires the following materials: {', '.join(required_materials)}")
            
            # Collect each required material
            for material in required_materials:
                while True:
                    if material == "text_prompt":
                        prompt = input("Please enter the text prompt: ")
                        if prompt.strip():
                            materials["text_prompt"] = prompt
                            break
                        else:
                            print("Text prompt cannot be empty. Please try again.")
                    elif material == "image_input":
                        image_url = input("Please enter the image URL: ")
                        if image_url.strip():
                            materials["image_input"] = image_url
                            break
                        else:
                            print("Image URL cannot be empty. Please try again.")
                    elif material == "video_input":
                        video_url = input("Please enter the video URL: ")
                        if video_url.strip():
                            materials["video_input"] = video_url
                            break
                        else:
                            print("Video URL cannot be empty. Please try again.")
                    elif material == "audio_input":
                        audio_url = input("Please enter the audio URL: ")
                        if audio_url.strip():
                            materials["audio_input"] = audio_url
                            break
                        else:
                            print("Audio URL cannot be empty. Please try again.")
                    elif material == "processing_params":
                        params = input("Please enter processing parameters: ")
                        if params.strip():
                            materials["processing_params"] = params
                            break
                        else:
                            print("Processing parameters cannot be empty. Please try again.")
        else:
            # If no materials were detected, ask if user wants to provide any
            print("No specific materials detected for this workflow.")
            add_materials = input("Do you want to provide any materials? (y/n): ")
            if add_materials.lower() == "y":
                # Offer common material options
                print("\nAvailable material types:")
                print("1. text_prompt (Text prompt)")
                print("2. image_input (Image URL)")
                print("3. video_input (Video URL)")
                print("4. audio_input (Audio URL)")
                print("5. processing_params (Processing parameters)")
                
                while True:
                    choice = input("\nEnter material type number (0 to finish): ")
                    if choice == "0":
                        break
                    elif choice == "1":
                        while True:
                            prompt = input("Please enter the text prompt: ")
                            if prompt.strip():
                                materials["text_prompt"] = prompt
                                break
                            else:
                                print("Text prompt cannot be empty. Please try again.")
                    elif choice == "2":
                        while True:
                            image_url = input("Please enter the image URL: ")
                            if image_url.strip():
                                materials["image_input"] = image_url
                                break
                            else:
                                print("Image URL cannot be empty. Please try again.")
                    elif choice == "3":
                        while True:
                            video_url = input("Please enter the video URL: ")
                            if video_url.strip():
                                materials["video_input"] = video_url
                                break
                            else:
                                print("Video URL cannot be empty. Please try again.")
                    elif choice == "4":
                        while True:
                            audio_url = input("Please enter the audio URL: ")
                            if audio_url.strip():
                                materials["audio_input"] = audio_url
                                break
                            else:
                                print("Audio URL cannot be empty. Please try again.")
                    elif choice == "5":
                        while True:
                            params = input("Please enter processing parameters: ")
                            if params.strip():
                                materials["processing_params"] = params
                                break
                            else:
                                print("Processing parameters cannot be empty. Please try again.")
                    else:
                        print("Invalid choice, please try again.")
        
        # Verify all required materials are collected
        if required_materials:
            missing_materials = [material for material in required_materials if material not in materials]
            if missing_materials:
                print(f"\nError: Missing required materials: {', '.join(missing_materials)}")
                print("Please provide all required materials to continue.")
                # Recursively collect missing materials
                for material in missing_materials:
                    while True:
                        if material == "text_prompt":
                            prompt = input("Please enter the text prompt: ")
                            if prompt.strip():
                                materials["text_prompt"] = prompt
                                break
                            else:
                                print("Text prompt cannot be empty. Please try again.")
                        elif material == "image_input":
                            image_url = input("Please enter the image URL: ")
                            if image_url.strip():
                                materials["image_input"] = image_url
                                break
                            else:
                                print("Image URL cannot be empty. Please try again.")
                        elif material == "video_input":
                            video_url = input("Please enter the video URL: ")
                            if video_url.strip():
                                materials["video_input"] = video_url
                                break
                            else:
                                print("Video URL cannot be empty. Please try again.")
                        elif material == "audio_input":
                            audio_url = input("Please enter the audio URL: ")
                            if audio_url.strip():
                                materials["audio_input"] = audio_url
                                break
                            else:
                                print("Audio URL cannot be empty. Please try again.")
                        elif material == "processing_params":
                            params = input("Please enter processing parameters: ")
                            if params.strip():
                                materials["processing_params"] = params
                                break
                            else:
                                print("Processing parameters cannot be empty. Please try again.")
        
        return materials
    
    def collect_workflow_inputs(self, required_inputs):
        """Collect inputs from user based on workflow analysis"""
        user_inputs = {}
        
        if not required_inputs:
            return user_inputs
        
        print(f"\nFound {len(required_inputs)} modifiable nodes in this workflow:")
        print("\nPlease select which nodes you want to configure:")
        
        for idx, node_info in enumerate(required_inputs, 1):
            node_id = node_info['node_id']
            class_type = node_info['class_type']
            title = node_info['title']
            node_inputs = node_info['inputs']
            
            print(f"\n{idx}. {title} (Node ID: {node_id}, Type: {class_type})")
            for input_info in node_inputs:
                key = input_info['key']
                input_type = input_info['type']
                input_title = input_info['title']
                current_value = input_info['current_value']
                print(f"   - {input_title} ({key}, Type: {input_type}): {current_value}")
        
        print("\nSelect nodes to configure (enter numbers separated by space, or 'all' for all):")
        selection = input("Your selection: ").strip()
        
        selected_indices = []
        if selection.lower() == 'all':
            selected_indices = list(range(1, len(required_inputs) + 1))
        else:
            try:
                selected_indices = [int(x.strip()) for x in selection.split() if x.strip().isdigit()]
            except ValueError:
                print("Invalid selection, will configure all nodes.")
                selected_indices = list(range(1, len(required_inputs) + 1))
        
        if not selected_indices:
            print("No nodes selected, will use default values for all.")
            return user_inputs
        
        print(f"\nConfiguring {len(selected_indices)} selected node(s):")
        print("Note: All selected inputs must be provided with valid values to continue.\n")
        
        for idx, node_info in enumerate(required_inputs, 1):
            if idx not in selected_indices:
                continue
            
            node_id = node_info['node_id']
            title = node_info['title']
            node_inputs = node_info['inputs']
            
            node_values = {}
            
            for input_info in node_inputs:
                key = input_info['key']
                input_type = input_info['type']
                input_title = input_info['title']
                current_value = input_info['current_value']
                
                while True:
                    print(f"\n{title} - {input_title} ({key}, Type: {input_type})")
                    print(f"   Current value: {current_value}")
                    use_current = input("   Use current value? (y/n): ")
                    if use_current.lower() == 'y':
                        node_values[key] = current_value
                        print(f"   ✓ Value set for {input_title}")
                        break
                    
                    if input_type == 'image':
                        image_input = input("   Enter image file path or URL: ")
                        
                        if self.is_url(image_input):
                            node_values[key] = image_input
                            print(f"   ✓ Using URL: {image_input}")
                            break
                        elif os.path.exists(image_input):
                            uploaded_filename = self.upload_file(image_input)
                            if uploaded_filename:
                                node_values[key] = uploaded_filename
                                print(f"   ✓ Image uploaded: {uploaded_filename}")
                                break
                        else:
                            print(f"   ✗ File not found: {image_input}")
                            print("   Please enter a valid file path or URL.")
                    
                    elif input_type == 'text':
                        text_value = input("   Enter text: ")
                        if text_value.strip():
                            node_values[key] = text_value
                            print(f"   ✓ Text set for {input_title}")
                            break
                        else:
                            print("   ✗ Text cannot be empty. Please try again.")
                    
                    elif input_type == 'number':
                        num_input = input(f"   Enter number: ")
                        if not num_input:
                            node_values[key] = current_value
                            print(f"   ✓ Using current value: {current_value}")
                            break
                        try:
                            num_value = float(num_input)
                            if num_value.is_integer():
                                num_value = int(num_value)
                            node_values[key] = num_value
                            print(f"   ✓ Value set to: {num_value}")
                            break
                        except ValueError:
                            print("   ✗ Please enter a valid number.")
            
            user_inputs[node_id] = node_values
        
        print(f"\n✓ All selected nodes have been configured successfully!")
        return user_inputs
    
    def build_node_info_list(self, workflow_json, user_inputs):
        """Build nodeInfoList for advanced workflow execution"""
        node_info_list = []
        
        for node_id, node_values in user_inputs.items():
            if node_id in workflow_json:
                node_info_list.append({
                    "nodeId": node_id,
                    "inputs": node_values
                })
        
        return node_info_list
    
    def execute_workflow(self, workflow_id, materials=None, webhook_url=None, node_info_list=None):
        """Execute ComfyUI workflow using Task 1 (Simple) or Task 2 (Advanced) API"""
        try:
            if node_info_list:
                payload = {
                    "workflowId": workflow_id,
                    "nodeInfoList": node_info_list
                }
                api_endpoint = f"{self.base_url}/comfyui/task2"
                print("Using Advanced API (Task 2) with custom inputs")
            else:
                payload = {
                    "workflowId": workflow_id
                }
                api_endpoint = f"{self.base_url}/comfyui/task1"
                print("Using Simple API (Task 1)")
            
            if materials:
                payload["materials"] = materials
            
            if webhook_url:
                payload["webhook"] = webhook_url
            
            response = requests.post(
                api_endpoint,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error executing workflow: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error executing workflow: {e}")
            return None
    
    def get_task_status(self, task_id):
        """Get task status"""
        try:
            response = requests.get(
                f"{self.base_url}/task/status",
                headers=self.headers,
                params={"taskId": task_id}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting task status: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error getting task status: {e}")
            return None
    
    def get_task_result(self, task_id):
        """Get task result"""
        try:
            response = requests.get(
                f"{self.base_url}/task/result",
                headers=self.headers,
                params={"taskId": task_id}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting task result: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error getting task result: {e}")
            return None
    
    def monitor_task(self, task_id, timeout=300):
        """Monitor task until completion or timeout"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            if status:
                task_status = status.get("status")
                print(f"Task status: {task_status}")
                
                if task_status == "completed":
                    return self.get_task_result(task_id)
                elif task_status in ["failed", "cancelled"]:
                    print(f"Task {task_status}")
                    return status
            
            time.sleep(5)
        
        print("Task timed out")
        return None

def main():
    """Main function"""
    print("ComfyUI Automation Skill")
    print("=" * 50)
    
    # Get API key from user
    api_key = input("Please enter your RunningHub API key: ")
    
    # Get workflow identifier from user
    workflow_identifier = input("Please enter workflow ID or nickname: ")
    
    # Create automation instance
    automation = ComfyUIAutomation(api_key)
    
    # Get workflow info
    print("\nGetting workflow information...")
    workflow_info = automation.get_workflow_info(workflow_identifier)
    
    if not workflow_info:
        print("Error: Workflow not found")
        return
    
    workflow_id = workflow_info.get("id")
    workflow_name = workflow_info.get("nickname", workflow_id)
    print(f"Found workflow: {workflow_name} (ID: {workflow_id})")
    
    # Get and analyze workflow JSON
    print("\nFetching and analyzing workflow structure...")
    workflow_json = automation.get_workflow_json(workflow_id)
    
    node_info_list = None
    if workflow_json:
        # Analyze workflow for required inputs
        required_inputs = automation.analyze_workflow_inputs(workflow_json)
        
        if required_inputs:
            # Collect inputs from user
            user_inputs = automation.collect_workflow_inputs(required_inputs)
            
            if user_inputs:
                # Build nodeInfoList for advanced execution
                node_info_list = automation.build_node_info_list(workflow_json, user_inputs)
                print(f"\nBuilt nodeInfoList with {len(node_info_list)} custom inputs")
    else:
        print("Warning: Could not fetch workflow JSON, using simple mode")
    
    # Collect materials (legacy mode)
    materials = None
    if not node_info_list:
        print("\nCollecting necessary materials...")
        materials = automation.collect_materials(workflow_info)
        
        # Request confirmation for materials
        if materials:
            print("\nMaterials collected:")
            for key, value in materials.items():
                print(f"- {key}: {value}")
    
    # Request confirmation
    confirmation = input("\nDo you want to execute this workflow? (y/n): ")
    if confirmation.lower() != "y":
        print("Execution cancelled")
        return
    
    # Execute workflow
    print("\nExecuting workflow...")
    webhook_url = input("Enter webhook URL (optional): ")
    
    if webhook_url.strip() == "":
        webhook_url = None
    
    task_response = automation.execute_workflow(workflow_id, materials, webhook_url, node_info_list)
    
    if not task_response:
        print("Error executing workflow")
        return
    
    task_id = task_response.get("taskId")
    if not task_id:
        print("Error: No task ID returned")
        return
    
    print(f"Task created with ID: {task_id}")
    
    # Monitor task
    print("\nMonitoring task execution...")
    result = automation.monitor_task(task_id)
    
    # Display result
    print("\nTask Result:")
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("No result available")

if __name__ == "__main__":
    main()