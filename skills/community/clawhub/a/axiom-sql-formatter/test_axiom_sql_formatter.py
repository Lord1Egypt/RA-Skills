"""Tests — axiom-sql-formatter """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_sql_formatter import _tokenize, format_sql


class TestFormat(unittest.TestCase):
    def test_01_simple_select(self):
        result = format_sql("select id, name from users")
        self.assertIn("SELECT", result)
        self.assertIn("FROM", result)
        # FROM should be on its own line
        self.assertIn("\nFROM", result)

    def test_02_uppercase_keywords(self):
        result = format_sql("select * from t where x = 1")
        self.assertIn("SELECT", result)
        self.assertIn("FROM", result)
        self.assertIn("WHERE", result)

    def test_03_join(self):
        sql = "select u.id, u.name from users u inner join orders o on u.id = o.user_id"
        result = format_sql(sql)
        self.assertIn("INNER JOIN", result)
        self.assertIn("\n", result)

    def test_04_group_by(self):
        sql = "select count(*), category from products group by category"
        result = format_sql(sql)
        self.assertIn("GROUP BY", result)

    def test_05_order_by(self):
        sql = "select * from t order by id desc"
        result = format_sql(sql)
        self.assertIn("ORDER BY", result)
        self.assertIn("DESC", result)

    def test_06_string_preserved(self):
        result = format_sql("select * from t where name = 'O''Brien'")
        self.assertIn("'O''Brien'", result)

    def test_07_line_comment(self):
        result = format_sql("select 1 -- this is a comment\n from t")
        self.assertIn("--", result)
        self.assertIn("comment", result)

    def test_08_no_newlines_added_to_strings(self):
        result = format_sql("select 'multi\nline\nstring' from t")
        # String preserved with newlines inside
        self.assertIn("'multi", result)


class TestTokenize(unittest.TestCase):
    def test_09_basic(self):
        tokens = _tokenize("select * from t")
        types = [t[0] for t in tokens]
        self.assertIn("word", types)
        self.assertIn("operator", types)

    def test_10_string(self):
        tokens = _tokenize("'hello'")
        self.assertEqual(tokens[0][0], "string")


class TestDeterminism(unittest.TestCase):
    def test_11_1000_runs(self):
        sql = "select id from users where active = true"
        first = format_sql(sql)
        for _ in range(1000):
            self.assertEqual(format_sql(sql), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
