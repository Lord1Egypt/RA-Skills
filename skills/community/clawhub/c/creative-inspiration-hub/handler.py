#!/usr/bin/env python3
import json, uuid, time
from typing import Dict, Any

ENGINE_VERSION = "cih-v1.2"

class InspirationHub:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.domains = self._load_domains()
    
    def _load_domains(self):
        return {
            "technology": {"concepts": ["人工智能", "区块链", "物联网"], "principles": ["自动化", "智能化"], "trends": ["AIGC", "元宇宙"]},
            "art": {"concepts": ["绘画", "雕塑", "装置艺术"], "principles": ["表达", "审美"], "trends": ["NFT艺术", "生成艺术"]},
            "science": {"concepts": ["物理学", "化学", "生物学"], "principles": ["观察", "实验"], "trends": ["脑科学", "基因编辑"]},
            "business": {"concepts": ["市场营销", "运营管理", "战略规划"], "principles": ["价值创造", "效率优化"], "trends": ["数字化转型", "平台经济"]},
            "design": {"concepts": ["工业设计", "平面设计", "用户体验设计"], "principles": ["功能美学", "以人为本"], "trends": ["情感化设计", "无障碍设计"]},
            "education": {"concepts": ["课程设计", "教学方法", "学习评估"], "principles": ["因材施教", "启发式教学"], "trends": ["微学习", "游戏化学习"]},
            "health": {"concepts": ["预防医学", "康复治疗", "心理健康"], "principles": ["预防为主", "整体观"], "trends": ["数字疗法", "精准医疗"]},
            "environment": {"concepts": ["气候变化", "生态系统", "资源循环"], "principles": ["生态优先", "循环经济"], "trends": ["碳中和", "零废弃"]},
            "entertainment": {"concepts": ["游戏", "影视", "音乐"], "principles": ["沉浸体验", "情感代入"], "trends": ["云游戏", "互动影视"]},
            "social": {"concepts": ["社区建设", "公共服务", "社会创新"], "principles": ["包容性", "参与性"], "trends": ["共享经济", "社会企业"]},
            "cultural": {"concepts": ["文化遗产", "博物馆", "民俗传统"], "principles": ["保护传承", "创新发展"], "trends": ["数字文博", "非遗新生"]}
        }
    
    def process(self, request):
        start = time.time()
        rtype = request.get("type", "idea-generation")
        if rtype == "idea-generation": result = self._gen_ideas(request)
        elif rtype == "cross-domain": result = self._cross_domain(request)
        elif rtype == "inspiration-trigger": result = self._gen_triggers(request)
        elif rtype == "evaluation": result = self._eval_idea(request)
        elif rtype == "mindmap": result = self._gen_mindmap(request)
        else: result = {"error": f"Unknown: {rtype}"}
        return {"success": True, "sessionId": f"session_{self.session_id}", **result, "metadata": {"requestType": rtype, "processingTime": int((time.time()-start)*1000), "model": ENGINE_VERSION, "engine": "local-rule-based"}}
    
    def _gen_ideas(self, req):
        theme = req.get("theme", "通用创意")
        domains = req.get("domains", ["technology"])
        ideas = []
        for i in range(3):
            d = domains[i % len(domains)]
            dd = self.domains.get(d, self.domains["technology"])
            ideas.append({"id": f"idea_{uuid.uuid4().hex[:6]}", "title": f"{theme}+{dd['concepts'][i]}", "description": f"结合{theme}和{d}，用{dd['principles'][0]}原则重新设计体验。", "origin": {"type": "cross-domain-combination", "sourceDomains": [d], "inspirationTriggers": dd["trends"]}, "evaluation": {"novelty": {"score": 7+(i%3), "rationale": "跨领域组合"}, "feasibility": {"score": 6+(i%4), "requirements": ["用户访谈", "低保真原型", "小范围验证"], "challenges": ["场景选择", "实现复杂度"]}, "value": {"score": 7+(i%3), "beneficiaries": ["目标用户", "产品团队"]}, "originality": {"score": 6+(i%4)}, "overall": 7+(i%2)}, "implementation": {"first_step": "用一个核心使用场景做纸面原型", "validation": "找3-5个目标用户进行反应测试"}, "potential": {"scalability": 7, "adaptability": 6, "sustainability": 7, "evolutionPaths": ["扩展", "升级"]}})
        return {"ideas": ideas}
    
    def _cross_domain(self, req):
        da, db = req.get("domainA", "technology"), req.get("domainB", "biology")
        scenario = req.get("applicationScenario", "创新应用")
        dda, ddb = self.domains.get(da, self.domains["technology"]), self.domains.get(db, self.domains["science"])
        pairs = [{"conceptA": dda["concepts"][i], "conceptB": ddb["concepts"][i], "relationship": f"{da}原理在{db}应用"} for i in range(min(3, len(dda["concepts"])))]
        return {"combinations": [{"id": f"combo_{uuid.uuid4().hex[:6]}", "domainA": da, "domainB": db, "combinationType": "fusion", "strength": 8, "synergy": 7, "inspirations": {"conceptPairs": pairs, "metaphorSuggestions": [f"像{dda['concepts'][0]}一样{ddb['principles'][0]}"], "applicationAreas": [scenario]}, "implementation": {"steps": ["调研", "寻找交叉点", "构建原型"], "tools": ["思维导图", "原型软件"], "skills": ["跨学科", "系统思考"]}}]}
    
    def _gen_triggers(self, req):
        words = [{"word": "转化", "category": "action", "semantics": {"connotations": ["转变"], "associations": ["蜕变"], "metaphors": ["蝴蝶破茧"]}}, {"word": "连接", "category": "action", "semantics": {"connotations": ["桥梁"], "associations": ["网络"], "metaphors": ["蛛网"]}}, {"word": "打破", "category": "action", "semantics": {"connotations": ["突破"], "associations": ["常规"], "metaphors": ["破冰"]}}, {"word": "融合", "category": "action", "semantics": {"connotations": ["混合"], "associations": ["化学反应"], "metaphors": ["调色板"]}}, {"word": "逆向", "category": "action", "semantics": {"connotations": ["反思"], "associations": ["反常识"], "metaphors": ["镜子"]}}]
        return {"triggers": [{"word": w["word"], "category": w["category"], "semantics": w["semantics"], "creativePotential": {"divergentThinking": 7+(i%3), "conceptualBreadth": 6+(i%4), "emotionalResonance": 7+(i%2)}} for i, w in enumerate(words[:5])]}
    
    def _eval_idea(self, req):
        idea = req.get("ideaToEvaluate", "创新想法")
        return {"evaluation": {"idea": idea, "scores": {"novelty": 7, "feasibility": 6, "value": 8, "originality": 7, "overall": 7}, "analysis": {"strengths": ["解决痛点", "有创新性"], "weaknesses": ["技术难度", "资源投入"], "improvementSuggestions": ["MVP验证", "差异化"], "risks": ["市场风险", "技术风险"]}, "recommendations": ["用户调研", "分阶段推出"]}}
    
    def _gen_mindmap(self, req):
        core = req.get("coreConcept", "创新")
        related = req.get("relatedThoughts", ["想法1", "想法2"])
        nodes = [{"id": "node_root", "content": core, "type": "concept", "importance": 10, "children": []}]
        for i, t in enumerate(related):
            cid = f"node_{i+1}"
            nodes.append({"id": cid, "content": t, "type": "concept", "importance": 7, "children": []})
            nodes[0]["children"].append(cid)
        return {"mindmap": {"title": f"{core}思维导图", "structure": {"layout": "radial", "depth": 2, "nodeCount": len(nodes)}, "nodes": nodes, "connections": [{"from": "node_root", "to": f"node_{i+1}", "type": "association", "strength": 8} for i in range(len(related))], "developmentSuggestions": ["扩展分支", "添加跨分支连接"]}}

def handle_request(req): return InspirationHub().process(req)

if __name__ == "__main__":
    print(json.dumps(handle_request({"type": "idea-generation", "theme": "智能家居", "domains": ["technology", "design"]}), ensure_ascii=False, indent=2))
