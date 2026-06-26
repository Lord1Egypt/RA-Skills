#!/usr/bin/env python3
import unittest, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from 12306_client import Railway12306Client

class TestRailway12306(unittest.TestCase):
    def test_login(self):
        if not all([os.getenv("RAILWAY_12306_USERNAME"), os.getenv("RAILWAY_12306_PASSWORD")]):
            self.skipTest("未配置")
        client = Railway12306Client(headless=True)
        client.start()
        try:
            self.assertTrue(client.login())
        finally:
            client.close()

if __name__ == "__main__":
    unittest.main()
