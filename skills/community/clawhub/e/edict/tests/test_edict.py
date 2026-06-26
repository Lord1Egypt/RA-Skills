# Edict 测试用例

import unittest
from edict import EdictSystem, ZhongshuProvince, MenxiaProvince, ShangshuProvince

class TestEdictSystem(unittest.TestCase):
    
    def setUp(self):
        """测试前初始化"""
        self.edict = EdictSystem()
    
    def test_system_initialization(self):
        """测试系统初始化"""
        self.assertIsNotNone(self.edict)
        self.assertTrue(hasattr(self.edict, 'zhongshu'))
        self.assertTrue(hasattr(self.edict, 'menxia'))
        self.assertTrue(hasattr(self.edict, 'shangshu'))
    
    def test_zhongshu_draft_proposal(self):
        """测试中书省草拟方案"""
        zhongshu = ZhongshuProvince()
        proposal = zhongshu.draft_proposal(
            task="测试任务",
            requirements=["要求1", "要求2"]
        )
        self.assertIsNotNone(proposal)
        self.assertIn("task", proposal)
    
    def test_menxia_review_proposal(self):
        """测试门下省审核方案"""
        menxia = MenxiaProvince()
        proposal = {"task": "测试", "requirements": []}
        review = menxia.review_proposal(proposal)
        self.assertIn("approved", review)
    
    def test_shangshu_decompose_task(self):
        """测试尚书省分解任务"""
        shangshu = ShangshuProvince()
        tasks = shangshu.decompose_task(
            project="测试项目",
            milestones=[{"name": "阶段1", "duration": "1周"}]
        )
        self.assertIsInstance(tasks, list)

class TestSixMinistries(unittest.TestCase):
    
    def test_libu_configure_agent(self):
        """测试吏部配置智能体"""
        from edict import Libu
        libu = Libu()
        agent = libu.configure_agent(
            name="测试智能体",
            role="test"
        )
        self.assertIsNotNone(agent)
    
    def test_hubu_allocate_budget(self):
        """测试户部分配预算"""
        from edict import Hubu
        hubu = Hubu()
        budget = hubu.allocate_budget(
            project="测试项目",
            amount=10000
        )
        self.assertEqual(budget["amount"], 10000)

if __name__ == '__main__':
    unittest.main()
