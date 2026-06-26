#!/usr/bin/env python3
"""
Execute a content workflow.

This script runs a workflow by executing each stage in sequence,
passing data between stages, and handling errors.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import importlib.util
import traceback

class WorkflowRunner:
    def __init__(self, workflow_file, input_data=None):
        self.workflow_file = Path(workflow_file)
        self.input_data = input_data or {}
        self.stage_results = {}
        self.current_stage = None
        
    def load_workflow(self):
        """Load workflow configuration from file."""
        if not self.workflow_file.exists():
            raise FileNotFoundError(f"Workflow file not found: {self.workflow_file}")
        
        with open(self.workflow_file, 'r') as f:
            self.workflow = json.load(f)
        
        print(f"📋 Loaded workflow: {self.workflow.get('name', 'Unnamed')}")
        print(f"   ID: {self.workflow.get('id', 'N/A')}")
        print(f"   Type: {self.workflow.get('type', 'custom')}")
        print(f"   Stages: {len(self.workflow.get('stages', []))}")
        
    def execute_stage(self, stage):
        """Execute a single workflow stage."""
        stage_name = stage['name']
        tool = stage['tool']
        config = stage.get('config', {})
        
        print(f"\n▶️  Executing stage: {stage_name}")
        print(f"   Tool: {tool}")
        
        # Prepare input for this stage
        stage_input = {
            **self.input_data,
            **self.stage_results,
            'config': config
        }
        
        # Record start time
        start_time = time.time()
        self.current_stage = stage_name
        
        try:
            # Execute the stage
            result = self._execute_tool(tool, stage_input)
            
            # Record result
            execution_time = time.time() - start_time
            self.stage_results[stage_name] = {
                'status': 'success',
                'result': result,
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ✅ Success ({execution_time:.2f}s)")
            if isinstance(result, dict) and 'summary' in result:
                print(f"   Summary: {result['summary']}")
            
            return True
            
        except Exception as e:
            # Record failure
            execution_time = time.time() - start_time
            self.stage_results[stage_name] = {
                'status': 'failed',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ❌ Failed ({execution_time:.2f}s): {e}")
            return False
    
    def _execute_tool(self, tool, input_data):
        """Execute a tool based on its name."""
        # This is a simplified version - in a real implementation,
        # each tool would have its own module or API client
        
        tool_handlers = {
            'ai-brainstorm': self._tool_ai_brainstorm,
            'ai-writer': self._tool_ai_writer,
            'ai-outliner': self._tool_ai_outliner,
            'grammar-check': self._tool_grammar_check,
            'seo-optimizer': self._tool_seo_optimizer,
            'wordpress': self._tool_wordpress,
            'social-media': self._tool_social_media,
            'content-calendar': self._tool_content_calendar,
            'social-scheduler': self._tool_social_scheduler,
            'analytics': self._tool_analytics,
            'content-aggregator': self._tool_content_aggregator,
            'ai-curator': self._tool_ai_curator,
            'template-filler': self._tool_template_filler,
            'email-service': self._tool_email_service,
            'email-analytics': self._tool_email_analytics,
            'ai-scriptwriter': self._tool_ai_scriptwriter,
            'tts': self._tool_tts,
            'video-editor': self._tool_video_editor,
            'youtube-upload': self._tool_youtube_upload,
        }
        
        if tool not in tool_handlers:
            # Try to load tool module
            tool_module = self._load_tool_module(tool)
            if tool_module:
                return tool_module.execute(input_data)
            else:
                raise ValueError(f"Unknown tool: {tool}")
        
        return tool_handlers[tool](input_data)
    
    def _load_tool_module(self, tool_name):
        """Load a tool module dynamically."""
        tool_path = Path(__file__).parent / "tools" / f"{tool_name}.py"
        if not tool_path.exists():
            return None
        
        try:
            spec = importlib.util.spec_from_file_location(tool_name, tool_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Warning: Failed to load tool module {tool_name}: {e}")
            return None
    
    # Tool implementations (simplified for prototype)
    def _tool_ai_brainstorm(self, input_data):
        """Generate content ideas."""
        topic = input_data.get('topic', 'content creation')
        count = input_data.get('config', {}).get('count', 5)
        
        # Simulate AI brainstorming
        ideas = [
            f"How {topic} is changing in 2025",
            f"5 tools for better {topic}",
            f"The future of {topic}: predictions",
            f"{topic.title()} best practices",
            f"Common mistakes in {topic} and how to avoid them"
        ][:count]
        
        return {
            'ideas': ideas,
            'count': len(ideas),
            'topic': topic,
            'summary': f"Generated {len(ideas)} ideas about {topic}"
        }
    
    def _tool_ai_writer(self, input_data):
        """Generate content based on input."""
        topic = input_data.get('topic', 'content workflow')
        tone = input_data.get('config', {}).get('tone', 'professional')
        
        # Simulate AI writing
        content = f"""# {topic.title()}: A Comprehensive Guide

{topic.title()} is revolutionizing how we create and distribute content. In this article, we'll explore the key aspects of effective {topic}.

## Why {topic.title()} Matters

In today's digital landscape, {topic} has become essential for scaling content production while maintaining quality.

## Key Benefits

1. **Increased Efficiency**: Automate repetitive tasks
2. **Consistent Quality**: Maintain brand voice across all content
3. **Better Analytics**: Track performance across platforms
4. **Time Savings**: Focus on strategy instead of execution

## Getting Started

Begin by identifying your most time-consuming content tasks and look for opportunities to automate them."""
        
        return {
            'content': content,
            'length': len(content),
            'tone': tone,
            'summary': f"Generated {len(content)} characters of {tone} content about {topic}"
        }
    
    def _tool_seo_optimizer(self, input_data):
        """Optimize content for SEO."""
        content = input_data.get('content', '')
        keywords = input_data.get('config', {}).get('keywords', [])
        
        # Simulate SEO optimization
        optimized = content
        if keywords:
            # Add keywords to first paragraph (simplified)
            first_para = optimized.split('\n\n')[0]
            if first_para:
                keyword_str = ', '.join(keywords[:3])
                optimized = optimized.replace(
                    first_para,
                    f"{first_para} This article covers {keyword_str} and related topics."
                )
        
        return {
            'optimized_content': optimized,
            'keywords_added': len(keywords),
            'summary': f"Optimized content with {len(keywords)} keywords"
        }
    
    def _tool_wordpress(self, input_data):
        """Publish to WordPress."""
        content = input_data.get('content', '')
        status = input_data.get('config', {}).get('status', 'draft')
        
        # Simulate WordPress publishing
        post_id = hash(content) % 10000  # Simulated post ID
        
        return {
            'post_id': post_id,
            'status': status,
            'url': f"https://example.com/?p={post_id}",
            'summary': f"Published to WordPress as {status} (ID: {post_id})"
        }
    
    def _tool_social_media(self, input_data):
        """Create social media posts."""
        content = input_data.get('content', '')
        platforms = input_data.get('config', {}).get('platforms', ['twitter'])
        
        # Simulate social media post creation
        snippets = {}
        for platform in platforms:
            if platform == 'twitter':
                snippet = content[:280] + ("..." if len(content) > 280 else "")
            elif platform == 'linkedin':
                snippet = content[:300] + ("..." if len(content) > 300 else "")
            else:
                snippet = content[:500] + ("..." if len(content) > 500 else "")
            
            snippets[platform] = snippet
        
        return {
            'snippets': snippets,
            'platforms': platforms,
            'summary': f"Created social snippets for {len(platforms)} platforms"
        }
    
    # Simplified implementations for other tools
    def _tool_ai_outliner(self, input_data):
        return {'outline': 'Generated outline', 'summary': 'Created content outline'}
    
    def _tool_grammar_check(self, input_data):
        return {'checked': True, 'issues': 0, 'summary': 'Grammar check completed'}
    
    def _tool_content_calendar(self, input_data):
        return {'calendar': 'Generated', 'summary': 'Content calendar created'}
    
    def _tool_social_scheduler(self, input_data):
        return {'scheduled': True, 'summary': 'Posts scheduled'}
    
    def _tool_analytics(self, input_data):
        return {'metrics': {}, 'summary': 'Analytics collected'}
    
    def _tool_content_aggregator(self, input_data):
        return {'content': [], 'summary': 'Content aggregated'}
    
    def _tool_ai_curator(self, input_data):
        return {'curated': [], 'summary': 'Content curated'}
    
    def _tool_template_filler(self, input_data):
        return {'filled': True, 'summary': 'Template filled'}
    
    def _tool_email_service(self, input_data):
        return {'sent': True, 'summary': 'Email sent'}
    
    def _tool_email_analytics(self, input_data):
        return {'analytics': {}, 'summary': 'Email analytics collected'}
    
    def _tool_ai_scriptwriter(self, input_data):
        return {'script': 'Generated', 'summary': 'Script written'}
    
    def _tool_tts(self, input_data):
        return {'audio': 'Generated', 'summary': 'Voiceover created'}
    
    def _tool_video_editor(self, input_data):
        return {'video': 'Edited', 'summary': 'Video edited'}
    
    def _tool_youtube_upload(self, input_data):
        return {'uploaded': True, 'summary': 'Video uploaded'}
    
    def run(self, stop_on_error=True):
        """Run the entire workflow."""
        self.load_workflow()
        
        print(f"\n🚀 Starting workflow execution")
        print(f"   Input: {json.dumps(self.input_data, indent=2)}")
        
        stages = self.workflow.get('stages', [])
        successful_stages = 0
        
        for i, stage in enumerate(stages, 1):
            print(f"\n--- Stage {i}/{len(stages)} ---")
            success = self.execute_stage(stage)
            
            if success:
                successful_stages += 1
            elif stop_on_error:
                print(f"\n⏹️  Stopping workflow due to stage failure")
                break
        
        # Generate execution report
        report = self.generate_report(successful_stages, len(stages))
        
        print(f"\n{'='*50}")
        print(f"Workflow Execution Complete")
        print(f"{'='*50}")
        print(f"Total stages: {len(stages)}")
        print(f"Successful: {successful_stages}")
        print(f"Failed: {len(stages) - successful_stages}")
        
        if successful_stages == len(stages):
            print(f"✅ Workflow completed successfully!")
        else:
            print(f"⚠️  Workflow completed with errors")
        
        return report
    
    def generate_report(self, successful, total):
        """Generate execution report."""
        report = {
            'workflow': self.workflow.get('id'),
            'name': self.workflow.get('name'),
            'execution_date': datetime.now().isoformat(),
            'total_stages': total,
            'successful_stages': successful,
            'failed_stages': total - successful,
            'stage_results': self.stage_results,
            'input_data': self.input_data,
            'final_output': self.stage_results
        }
        
        # Save report
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"{self.workflow.get('id')}_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Report saved: {report_file}")
        return report_file

def main():
    parser = argparse.ArgumentParser(description="Run a content workflow")
    parser.add_argument("--workflow", required=True, help="Workflow ID or path to workflow file")
    parser.add_argument("--input", help="Input data as JSON string")
    parser.add_argument("--input-file", help="Path to JSON file with input data")
    parser.add_argument("--continue-on-error", action="store_true", 
                       help="Continue execution even if a stage fails")
    
    args = parser.parse_args()
    
    # Load input data
    input_data = {}
    if args.input:
        try:
            input_data = json.loads(args.input)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON input: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                input_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading input file: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Determine workflow file path
    workflow_file = args.workflow
    if not Path(workflow_file).exists():
        # Try to find in workflows directory
        workflow_file = Path("workflows") / f"{args.workflow}.json"
        if not workflow_file.exists():
            print(f"❌ Workflow not found: {args.workflow}", file=sys.stderr)
            sys.exit(1)
    
    # Run workflow
    try:
        runner = WorkflowRunner(workflow_file, input_data)
        report_file = runner.run(stop_on_error=not args.continue_on_error)
        
        print(f"\n🎯 Final output available in: {report_file}")
        
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()