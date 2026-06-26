---
name: algo-practice
description: 🎯 Interactive algorithm practice with 100+ problems across Easy/Medium/Hard difficulties. Generates ready-to-run code templates in Java & Python with built-in test cases. Perfect for coding interview preparation and algorithm learning. Covers arrays, strings, linked lists, trees, dynamic programming, graphs, and more.
---

# 🎯 Algo Practice - Interactive Algorithm Training

Transform your coding interview preparation with curated algorithm problems, auto-generated code templates, and instant test feedback.

## ✨ Features

- **📚 100+ Algorithm Problems** - Carefully selected from classic interview questions
- **🎚️ Three Difficulty Levels** - Easy, Medium, Hard with progressive learning path
- **💻 Dual Language Support** - Java & Python templates with identical test cases
- **✅ Built-in Testing** - 5-8 test cases per problem including edge cases
- **📊 Progress Tracking** - Auto-maintained history to avoid duplicates
- **🎓 Learning Oriented** - Hints provided without giving away solutions
- **🚀 Ready to Run** - Complete code templates with main entry points

## 🚀 Quick Start

### Basic Usage
```
User: 出算法题 / 刷题 / 练算法 / algo practice / 来一道题
```

The skill will:
1. Ask for your preferred difficulty level
2. Generate a unique problem you haven't seen
3. Create ready-to-code templates in both Java and Python
4. Track your progress automatically

### Example Interaction
```
User: 刷题
AI: [Asks for difficulty preference]
User: Medium
AI: [Generates problem with templates]
```

## 📋 Workflow

### Step 1: Check Problem History

Read `algo_history.md` from the workspace root to track previously assigned problems and ensure no duplicates.

```markdown
# Algorithm Practice History

| # | Problem Name | Difficulty | Category | Date |
|---|-------------|------------|----------|------|
| 1 | TwoSum | Easy | Array, Hash Table | 2026-03-27 |
```

### Step 2: Ask Difficulty Preference

Use the `AskUserQuestion` tool:

**Question**: "Which difficulty level would you like?"

**Options**:
- **🟢 Easy** - Basic data structures & simple logic, perfect for warm-up
- **🟡 Medium** - Requires algorithmic thinking, covers common patterns
- **🔴 Hard** - Advanced algorithms, optimization, complex data structures

### Step 3: Generate Problem

Create an **original algorithm problem** with:

#### Problem Structure
- **Title**: PascalCase format (e.g., `LongestSubstring`, `MergeIntervals`)
- **Difficulty Badge**: 🟢 Easy / 🟡 Medium / 🔴 Hard
- **Description**: Clear Chinese explanation of input/output requirements
- **Examples**: Minimum 2 examples with input/output pairs
- **Constraints**: Data ranges, time/space complexity requirements
- **Hints**: Direction hints without revealing the solution

#### Problem Categories (Rotate through these)
Arrays, Strings, Linked Lists, Trees, Graphs, Dynamic Programming, Greedy, Backtracking, Sorting, Searching, Stack/Queue, Hash Tables, Two Pointers, Sliding Window, Bit Manipulation, BFS/DFS, Divide & Conquer

### Step 4: Create Code Templates

#### Java Template: `java/<ProblemName>.java`

```java
import java.util.*;

public class <ProblemName> {

    /**
     * TODO: Implement your algorithm here
     *
     * <Brief description of function>
     *
     * @param <parameter description>
     * @return <return value description>
     */
    public <ReturnType> <methodName>(<Parameters>) {
        // Write your code here
        return <default value>;
    }

    public static void main(String[] args) {
        <ProblemName> solution = new <ProblemName>();
        int passed = 0;
        int total = 0;

        // Test Case 1: Normal case
        total++;
        <Type> result1 = solution.<methodName>(<input1>);
        if (<check if result1 equals expected1>) {
            System.out.println("Test Case " + total + ": ✅ Pass");
            passed++;
        } else {
            System.out.println("Test Case " + total + ": ❌ Fail");
            System.out.println("  Input: <input description>");
            System.out.println("  Expected: <expected output>");
            System.out.println("  Actual: " + result1);
        }

        // Test Case 2-N: Include edge cases (minimum 5 total)
        // Must cover: normal cases, boundary cases, special cases

        System.out.println("\nResults: " + passed + "/" + total + " Passed");
        if (passed == total) {
            System.out.println("🎉 All tests passed!");
        } else {
            System.out.println("💪 Keep trying! Review the failed cases above.");
        }
    }
}
```

#### Python Template: `python/<problem_name>.py`

```python
from typing import List, Optional


class Solution:
    def <method_name>(self, <parameters>) -> <return_type>:
        """
        TODO: Implement your algorithm here

        <Brief description of function>

        Args:
            <parameter description>

        Returns:
            <return value description>
        """
        # Write your code here
        pass


def main():
    solution = Solution()
    passed = 0
    total = 0

    # Test Case 1: Normal case
    total += 1
    result1 = solution.<method_name>(<input1>)
    if result1 == <expected1>:
        print(f"Test Case {total}: ✅ Pass")
        passed += 1
    else:
        print(f"Test Case {total}: ❌ Fail")
        print(f"  Input: <input description>")
        print(f"  Expected: <expected output>")
        print(f"  Actual: {result1}")

    # Test Case 2-N: Include edge cases (minimum 5 total)
    # Must cover: normal cases, boundary cases, special cases

    print(f"\nResults: {passed}/{total} Passed")
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("💪 Keep trying! Review the failed cases above.")


if __name__ == "__main__":
    main()
```

#### Test Case Requirements
- **Minimum 5 test cases** per problem
- **Must include**:
  - Normal/typical cases
  - Edge cases (empty input, single element, maximum values)
  - Special cases (negative numbers, duplicates, etc.)
- **Consistency**: Java and Python test cases must match
- **Proper comparison**: Use `Arrays.equals()` for Java arrays, `==` for Python lists

### Step 5: Update Progress Tracking

Append the problem to `algo_history.md` in workspace root:

```markdown
# Algorithm Practice History

| # | Problem Name | Difficulty | Category | Date |
|---|-------------|------------|----------|------|
| 1 | TwoSum | Easy | Array, Hash Table | 2026-03-27 |
| 2 | MergeIntervals | Medium | Array, Sorting | 2026-03-27 |
```

Auto-increment the sequence number and use current date.

### Step 6: Present Problem to User

Display the complete problem with:

1. **📝 Problem Title & Difficulty Badge**
2. **📖 Problem Description** (clear Chinese explanation)
3. **💡 Examples** (input/output pairs)
4. **⚙️ Constraints** (data ranges, complexity requirements)
5. **🎯 Hints** (direction without solution)
6. **📁 File Locations**:
   - Java: `java/<ProblemName>.java`
   - Python: `python/<problem_name>.py`
7. **🚀 Next Steps**: "Implement your solution and run the file to test!"

## 💡 Pro Tips for Users

### How to Use Effectively
1. **Start Easy** - Build confidence with fundamentals
2. **Think First** - Try to solve before looking at hints
3. **Test Thoroughly** - Run both Java and Python versions
4. **Track Progress** - Check `algo_history.md` for your journey
5. **Practice Regularly** - Consistency beats intensity

### Running Your Solutions
```bash
# Java
cd java
javac <ProblemName>.java && java <ProblemName>

# Python
python python/<problem_name>.py
```

### Common Workflow
1. Read problem carefully
2. Think about approach (don't code immediately!)
3. Write solution in the TODO section
4. Run tests to verify
5. Debug failed cases
6. Optimize if needed
7. Move to next problem

## 🎯 Problem Quality Standards

- ✅ **Interview-Relevant**: Based on real coding interview questions
- ✅ **Well-Tested**: 5-8 comprehensive test cases
- ✅ **Progressive Difficulty**: Clear learning path
- ✅ **No Duplicates**: Tracked via history file
- ✅ **Bilingual**: Java + Python with consistent logic
- ✅ **Production-Ready**: Ready to compile and run

## 🛠️ Technical Requirements

- Method signatures must be clear and type-safe
- Java filename MUST match public class name
- Python filename uses snake_case convention
- Problem titles use PascalCase (e.g., `ValidParentheses`)
- NEVER include solutions or implementation hints in code files
- Test case expected outputs MUST be correct
- Create `java/` and `python/` directories if they don't exist

## 🌟 Target Audience

- 👨‍💻 Job seekers preparing for coding interviews
- 🎓 Computer science students learning algorithms
- 🔄 Developers wanting to practice problem-solving
- 🌱 Beginners starting their algorithm journey
- 🏆 Advanced programmers tackling hard problems

## 📊 Success Metrics

After using this skill, users should:
- Have working code templates ready to implement
- Understand the problem clearly with examples
- Know the constraints and edge cases
- Feel motivated to solve and test their solution
- Track their progress over time

---

**💡 Tip**: This skill is perfect for daily algorithm practice. Try solving 1-2 problems per day to build strong problem-solving skills!
