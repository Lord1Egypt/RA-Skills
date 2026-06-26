import unittest

from scripts import databricks_helper as helper


class SqlSafetyTests(unittest.TestCase):
    def test_select_is_safe(self):
        self.assertTrue(helper.is_sql_safe("SELECT * FROM table"))

    def test_insert_blocked(self):
        self.assertFalse(helper.is_sql_safe("INSERT INTO table VALUES (1)"))

    def test_limit_wrap_added(self):
        query = "SELECT * FROM demo"
        wrapped = helper.apply_sql_limit(query, 50)
        self.assertIn("LIMIT 50", wrapped)
        self.assertTrue(wrapped.lower().startswith("select * from (select"))

    def test_limit_ignored_for_show(self):
        query = "SHOW TABLES"
        self.assertEqual(helper.apply_sql_limit(query, 10), query)


class JobFilterTests(unittest.TestCase):
    def setUp(self):
        self.jobs = [
            {"job_id": 1, "settings": {"name": "Daily ETL", "tags": {"env": "prod"}}},
            {"job_id": 2, "settings": {"name": "Adhoc QA", "tags": {"env": "qa"}}},
            {"job_id": 3, "settings": {"name": "Daily Finance", "tags": {"team": "fin"}}},
        ]

    def test_pattern_filter(self):
        results = helper.filter_jobs(self.jobs, "daily", {})
        self.assertEqual({job["job_id"] for job in results}, {1, 3})

    def test_tag_filter(self):
        results = helper.filter_jobs(self.jobs, None, {"env": "prod"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["job_id"], 1)


if __name__ == "__main__":
    unittest.main()
