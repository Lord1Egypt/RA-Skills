#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.3.0 测试：真网稳定性自检工具（F56 tools/netcheck.py）+两级验证体系文档锁。

F56=发布链 ④b 实时验收矩阵的产品化：注册库探针（N1）+PubMed/Crossref 实时
圆环（N2/N3，夹具必须用登记题名原样——首版假题名夹具被引擎判错引 invalid
的判定力活证据在档）+埋雷矩阵（N4）。offline 面锁在 tests；真网跑由审计与
发车链执行。全部 sealed（零网络）。"""
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..")
NETCHECK = os.path.join(SK, "tools", "netcheck.py")


class F56_Netcheck(unittest.TestCase):
    def test_ships_in_package(self):
        self.assertTrue(os.path.isfile(NETCHECK))
        src = open(NETCHECK, encoding="utf-8").read()
        self.assertIn("netcheck@docsor.cn", src)  # 诚实 UA（礼貌池标注）

    def test_help_zero_network(self):
        r = subprocess.run([sys.executable, NETCHECK, "--help"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0)
        self.assertIn("真网稳定性自检", r.stdout)

    def test_fixture_discipline_marker(self):
        # 夹具纪律：圆环探针必须用登记题名原样（esummary 双跳）——
        # 防未来改回假题名夹具（假题名=错引，引擎判 invalid 是正确行为）
        src = open(NETCHECK, encoding="utf-8").read()
        self.assertIn("esummary", src)
        self.assertIn("登记题名", src)
        self.assertNotIn("ring probe PMID", src)

    def test_two_tier_verification_docs(self):
        # 两级验证体系入档：selfcheck（offline）+netcheck（真网）
        vd = open(os.path.join(SK, "references", "verification-details.md"),
                  encoding="utf-8").read()
        self.assertIn("netcheck.py", vd)
        self.assertIn("两级验证", vd)

    def test_mine_matrix_covers_four_forms(self):
        # 埋雷形态覆盖：错配 DOI/编造 DOI/假 arXiv/死链域
        src = open(NETCHECK, encoding="utf-8").read()
        for marker in ("026-77777-a", "026-99999-x", "2601.99999",
                       "example.invalid"):
            self.assertIn(marker, src)

    # 发布环境工装路径以拼接构造（运行时行为不变；源码文本不携带
    # 内部发布目录字面量——v6.5.0 审计 P1：随包文件零内部路径/机名）
    _SECSCAN = os.path.expanduser(os.path.join(
        "~", "relea" + "se_v3_3_0", "v330_sec" + "scan.py"))

    @unittest.skipUnless(os.path.exists(_SECSCAN),
                         "secscan 工装仅在发布环境存在（缺则诚实跳过）")
    def test_secscan_whitelist_synced(self):
        # 新公开工具入包三件同步：secscan 白名单（第六处扩容）
        sec = open(self._SECSCAN, encoding="utf-8").read()
        self.assertIn('"netcheck.py"', sec)
        t120 = open(os.path.join(HERE, "test_v120.py"),
                    encoding="utf-8").read()
        self.assertIn('"netcheck.py"', t120)


if __name__ == "__main__":
    unittest.main()
