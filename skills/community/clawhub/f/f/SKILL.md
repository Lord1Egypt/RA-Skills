#### Skill: SQL Operations Mastery

**Name:** `sql-operations-mastery`
**Description:** A comprehensive guide to performing database operations using SQL, covering data definition, manipulation, querying, and control in relational database systems.
**Keywords:** ["sql", "database", "relational database", "data manipulation", "data definition", "query", "mysql", "postgresql", "oracle"]

#### SQL Operations Mastery

**Objective**
To equip users with the practical skills needed to effectively create, manage, and query relational databases using standard SQL (Structured Query Language).

#### Core Concept: The Language of Data

SQL (Structured Query Language) is the standardized programming language used to manage and manipulate relational databases. It is a **declarative language**, meaning you specify *what* data you want, and the database management system (DBMS) figures out the most efficient way to retrieve it.

- **Relational Databases:** Data is organized into **tables** (relations) consisting of **rows** (records) and **columns** (fields). Tables can be linked via **keys** (primary and foreign keys).
- **Universal Application:** While different database systems like MySQL, PostgreSQL, Oracle, and SQL Server have their own extensions (e.g., T-SQL), the core SQL syntax is largely consistent across all platforms.

#### The Four Pillars of SQL Commands

SQL commands are categorized into four main types based on their function.

**Data Definition Language (DDL)**
DDL commands are used to define and manage the structure of the database and its objects, such as tables and indexes.

- **CREATE:** Used to create new database objects.
    - **Create a Database:**

```
CREATE DATABASE my_company;
```

    - **Create a Table:**

```
USE my_company;
CREATE TABLE employees (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10, 2)
);
```

- **ALTER:** Used to modify the structure of an existing object.
    - **Add a Column:**

```
ALTER TABLE employees ADD COLUMN department VARCHAR(50);
```

- **DROP:** Used to delete an entire object from the database.
    - **Delete a Table:**

```
DROP TABLE employees;
```

**Data Manipulation Language (DML)**
DML commands are used to insert, update, and delete the actual data within the tables.

- **INSERT:** Adds new rows of data to a table.

```
INSERT INTO employees (id, first_name, last_name, hire_date, salary, department)
VALUES (101, 'Jane', 'Doe', '2023-01-15', 75000.00, 'Engineering');
```

- **UPDATE:** Modifies existing data in a table.

```
UPDATE employees
SET salary = 80000.00
WHERE id = 101;
```

- **DELETE:** Removes rows from a table.

```
DELETE FROM employees
WHERE id = 101;
```

**Data Query Language (DQL)**
DQL is primarily used for retrieving data from the database. The `SELECT` statement is the cornerstone of DQL.

- **Basic Query:** Retrieve specific columns from a table.

```
SELECT first_name, last_name FROM employees;
```

- **Filtering with WHERE:** Retrieve data that meets specific criteria.

```
SELECT * FROM employees WHERE department = 'Engineering';
```

- **Sorting with ORDER BY:** Sort the result set by one or more columns.

```
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;
```

**Data Control Language (DCL)**
DCL commands manage access rights and permissions to the database.

- **GRANT:** Gives a user specific privileges.

```
GRANT SELECT, INSERT ON employees TO 'analyst_user';
```

- **REVOKE:** Takes away privileges from a user.

```
REVOKE INSERT ON employees FROM 'analyst_user';
```

#### Advanced Querying Techniques

To extract meaningful insights, you often need to perform more complex queries.

**Aggregating Data**
Aggregate functions perform a calculation on a set of values and return a single value. Common functions include `COUNT()`, `SUM()`, `AVG()`, `MIN()`, and `MAX()`.

- **Example:** Find the average salary in the Engineering department.

```
SELECT AVG(salary) AS average_salary
FROM employees
WHERE department = 'Engineering';
```

- **Grouping with GROUP BY:** Used with aggregate functions to group results by one or more columns.

```
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;
```

**Combining Data from Multiple Tables (JOINs)**
The `JOIN` clause is used to combine rows from two or more tables based on a related column between them.

- **INNER JOIN:** Returns records that have matching values in both tables.

```
-- Assume we have a 'departments' table with dept_id and dept_name
SELECT e.first_name, e.last_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.department = d.dept_name;
```

**Subqueries**
A subquery is a query nested inside another query. It is often used in a `WHERE` clause.

- **Example:** Find employees whose salary is above the company's average salary.

```
SELECT first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

#### Best Practices for Safe and Efficient Operations

- **Always Use WHERE for UPDATE/DELETE:** Forgetting the `WHERE` clause in an `UPDATE` or `DELETE` statement will apply the operation to **every row** in the table. This is a common and often catastrophic mistake.
- **Use Transactions for Data Integrity:** A transaction groups a set of SQL statements into a single unit of work. Either all statements succeed, or none of them do. This is crucial for maintaining data consistency.

```
BEGIN; -- Start the transaction
UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;
COMMIT; -- Save all changes
-- If an error occurs, you can use ROLLBACK; to undo all changes
```

- **Use Parameterized Queries:** When writing application code that interacts with the database, always use parameterized queries to prevent **SQL injection** attacks, where malicious SQL code is inserted into a query.
- **Indexing for Performance:** Create indexes on columns that are frequently used in `WHERE` clauses and `JOIN` conditions to significantly speed up query performance.

```
CREATE INDEX idx_employee_dept ON employees(department);
```

