import os, sys

sys.path.insert(0, r"D:\类脑记忆\CNexus2.0")
from src.kernel import CNexusOSKernel
from src.data_pipeline import DataPipeline
from src.calibrator import PersonaCalibrator
from src.llm_adapter import LLMAdapter


class CNexusOSCoreEngine:
    """CNexus 2.0 顶层核心引擎 - 彻底隔离外部框架依赖"""
    def __init__(self):
        self.kernel = CNexusOSKernel()
        self.pipeline = DataPipeline()
        self.calibrator = PersonaCalibrator()
        self.speaker = LLMAdapter()
        self.is_initialized = False

    def initialize(self) -> bool:
        base_path = r"D:\类脑记忆\CNexus2.0\config"
        class_file = os.path.join(base_path, "class.json")
        router_file = os.path.join(base_path, "router.json")
        graph_file = os.path.join(base_path, "graph.json")

        if not os.path.exists(class_file):
            print("[CNexus2.0] 未检测到引导文件，启动虚空静态资产分配。")
            self.is_initialized = True
            return True

        if self.kernel.boot(class_file, router_file, graph_file):
            self.kernel.reset()
            self.is_initialized = True
            return True
        return False

    def import_file_to_memory(self, file_path: str) -> dict:
        if not self.is_initialized:
            self.initialize()
        try:
            memory_blocks = self.pipeline.process(file_path)
            profile = self.calibrator.analyze_profile(memory_blocks)
            self.calibrator.apply_to_kernel(self.kernel, profile)
            for block in memory_blocks:
                self.kernel.memory_store[block['block_id']] = block
            return {
                "status": "success",
                "imported_blocks_count": len(memory_blocks),
                "calibrated_profile": profile
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def handle_request(self, input_text: str) -> str:
        if not self.is_initialized:
            self.initialize()
        kernel_output = self.kernel.run(input_text)

        matched = []
        for b in self.kernel.memory_store.values():
            output = b['content']['output']
            if any(kw in input_text for kw in output[:3]):
                matched.append(b['content'])
        kernel_output['execution_results'] = matched[:2]

        kernel_output['cog_state'] = {
            'accumulated_weight': self.kernel.cog['cog_state'].get('accumulated_weight', 0.5),
            'current_intent': self.kernel.cog['cog_state'].get('current_intent', 'converse')
        }

        system_p, user_p = self.speaker.render_prompt(kernel_output, input_text)
        return self.speaker.generate_via_ollama(system_p, user_p)
