"""
🛠️ axiom-sql-formatter — SQL Formatter
=========================================

⚠️ LIMITATIONS CONNUES :
- Pas de CTE récursifs (WITH RECURSIVE)
- Pas de window functions avancées
- Pas de support multi-statement (split par `;`)

FORMATE LES REQUÊTES SQL AVEC INDENTATION CORRECTE
"""

import re
import sys


# SQL keywords that start a new line at the top level
TOP_LEVEL_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "HAVING",
    "LIMIT", "OFFSET", "UNION", "UNION ALL", "INTERSECT", "EXCEPT",
    "INSERT INTO", "VALUES", "UPDATE", "SET", "DELETE FROM",
    "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "OUTER JOIN",
    "FULL JOIN", "CROSS JOIN", "ON",
}

# SQL keywords that are always uppercase
KEYWORDS = {
    "SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "IN", "IS", "NULL",
    "LIKE", "BETWEEN", "EXISTS", "ALL", "ANY", "SOME",
    "AS", "ON", "USING", "JOIN", "INNER", "LEFT", "RIGHT", "OUTER",
    "FULL", "CROSS", "NATURAL",
    "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "OFFSET", "ASC", "DESC",
    "UNION", "INTERSECT", "EXCEPT", "ALL", "DISTINCT",
    "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "INDEX", "VIEW", "DROP", "ALTER", "ADD",
    "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "UNIQUE", "CHECK",
    "DEFAULT", "NOT", "AUTO_INCREMENT", "SERIAL",
    "CASE", "WHEN", "THEN", "ELSE", "END",
    "BEGIN", "COMMIT", "ROLLBACK", "TRANSACTION",
    "WITH", "RECURSIVE", "OVER", "PARTITION", "BY",
    "TRUE", "FALSE",
}


def _tokenize(sql: str) -> list:
    """
    Tokenize SQL into (type, value) tuples.

    Types: word, string, number, operator, punctuation, comment
    """
    tokens = []
    i = 0
    n = len(sql)

    while i < n:
        ch = sql[i]

        # Whitespace
        if ch.isspace():
            j = i
            while j < n and sql[j].isspace():
                j += 1
            tokens.append(("whitespace", sql[i:j]))
            i = j
            continue

        # Line comment --
        if ch == "-" and i + 1 < n and sql[i+1] == "-":
            j = sql.find("\n", i)
            if j == -1:
                j = n
            tokens.append(("comment", sql[i:j]))
            i = j
            continue

        # Block comment /* */
        if ch == "/" and i + 1 < n and sql[i+1] == "*":
            j = sql.find("*/", i)
            if j == -1:
                j = n
            else:
                j += 2
            tokens.append(("comment", sql[i:j]))
            i = j
            continue

        # String literal
        if ch in ("'", '"'):
            quote = ch
            j = i + 1
            while j < n:
                if sql[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if sql[j] == quote:
                    if j + 1 < n and sql[j+1] == quote:  # escaped quote
                        j += 2
                        continue
                    j += 1
                    break
                j += 1
            tokens.append(("string", sql[i:j]))
            i = j
            continue

        # Number
        if ch.isdigit() or (ch == "." and i + 1 < n and sql[i+1].isdigit()):
            j = i
            while j < n and (sql[j].isdigit() or sql[j] == "."):
                j += 1
            tokens.append(("number", sql[i:j]))
            i = j
            continue

        # Word (identifier or keyword)
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (sql[j].isalnum() or sql[j] == "_"):
                j += 1
            word = sql[i:j]
            tokens.append(("word", word))
            i = j
            continue

        # Operators and punctuation
        if ch in "(),;*<>!=":
            j = i
            while j < n and sql[j] in "(),;*<>!=":
                j += 1
            tokens.append(("operator", sql[i:j]))
            i = j
            continue

        # Anything else
        tokens.append(("other", ch))
        i += 1

    return tokens


def _format_tokens(tokens: list) -> str:
    """Format tokens into a nicely indented SQL string."""
    # First pass: combine multi-word keywords (GROUP BY, ORDER BY, etc.)
    combined = []
    i = 0
    while i < len(tokens):
        tok_type, tok_value = tokens[i]

        if tok_type == "word":
            # Check for multi-word keyword
            upper = tok_value.upper()
            if upper in ("GROUP", "ORDER") and i + 2 < len(tokens):
                next_tok_type, next_tok_value = tokens[i+2]
                if next_tok_type == "word" and next_tok_value.upper() == "BY":
                    combined.append(("word", upper + " " + next_tok_value.upper()))
                    i += 3
                    continue
            elif upper in ("LEFT", "RIGHT", "INNER", "OUTER", "FULL", "CROSS") and i + 2 < len(tokens):
                next_tok_type, next_tok_value = tokens[i+2]
                if next_tok_type == "word" and next_tok_value.upper() == "JOIN":
                    combined.append(("word", upper + " " + next_tok_value.upper()))
                    i += 3
                    continue
            elif upper == "UNION" and i + 2 < len(tokens):
                next_tok_type, next_tok_value = tokens[i+2]
                if next_tok_type == "word" and next_tok_value.upper() == "ALL":
                    combined.append(("word", "UNION ALL"))
                    i += 3
                    continue

            # Uppercase keywords, preserve case for identifiers
            if upper in KEYWORDS:
                combined.append(("word", upper))
            else:
                combined.append(("word", tok_value))
        else:
            combined.append((tok_type, tok_value))
        i += 1

    # Second pass: add line breaks before top-level keywords
    output = []
    newline_keywords = TOP_LEVEL_KEYWORDS | {
        "AND", "OR",  # AND/OR usually get their own line in WHERE
    }

    for i, (tok_type, tok_value) in enumerate(combined):
        if tok_type == "whitespace":
            continue  # We'll add our own whitespace

        if tok_type == "word" and tok_value in newline_keywords:
            # Add newline before
            if output and not output[-1].endswith("\n"):
                output.append("\n")
            output.append(tok_value)
            output.append(" ")
        elif tok_type == "operator" and tok_value == ",":
            # Comma at end of line
            output.append(",\n  ")
        elif tok_type == "operator" and tok_value == ";":
            output.append(";\n")
        elif tok_type == "comment":
            # Comments go on their own line
            if output and not output[-1].endswith("\n"):
                output.append("\n")
            output.append(tok_value)
            output.append("\n")
        else:
            output.append(tok_value)
            if tok_type != "operator" or tok_value not in "(,)":
                output.append(" ")

    result = "".join(output)
    # Cleanup: multiple spaces, trailing whitespace
    result = re.sub(r" +", " ", result)
    result = re.sub(r" *\n *", "\n", result)
    result = re.sub(r"\n+", "\n", result)
    return result.strip()


def format_sql(sql: str) -> str:
    """Format a SQL query."""
    tokens = _tokenize(sql)
    return _format_tokens(tokens)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-sql-formatter ")
    parser.add_argument("sql", nargs="?", help="SQL to format")
    parser.add_argument("--file", help="Read SQL from file")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            sql = f.read()
        print(format_sql(sql))
        return 0

    if not args.sql:
        # Demo
        demo = """select id, name, email from users where active = true and created_at > '2024-01-01' order by created_at desc limit 100"""
        print(format_sql(demo))
        return 0

    print(format_sql(args.sql))
    return 0


if __name__ == "__main__":
    sys.exit(main())
