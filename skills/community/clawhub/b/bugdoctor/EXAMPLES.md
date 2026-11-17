# BugDoctor examples

## Read the useful logs

GPT-6.1 Sol, October 12, 2026. A controlled export incident used 4,509 interleaved log records. The request was:

> Job J42 ended with RETRY_EXHAUSTED and produced two export objects. Diagnose what happened and recommend the next useful action. Do not change files.

Plain Sol, the earlier BugDoctor and two debugging skills all diagnosed it correctly, but first emitted the entire log. One evidence-selection paragraph changed that behavior while preserving the diagnosis and source pointers.

| Captured tool-output characters | Earlier BugDoctor | Evidence-selection change |
| --- | --- | --- |
| First trial | 957,851 | 5,699 |
| Independent repeat of the same incident | 957,651 | 6,097 |

The combined candidate also avoided the full-file dump. Native OpenClaw read the new skill and workflow guide and returned:

> J42’s exports succeeded; notification failed. Retrying from the beginning created the second export.

The useful action was to reconcile the existing objects and recover notification, preserving the completed storage operation. Captured output size does not measure model tokens, price or accuracy. The new repair cases otherwise tied with baseline and the compared skills.

## Earlier repair comparisons

Earlier BugDoctor candidate, GPT-6.1 Sol tests, October 8, 2026. These use historical SymPy reports from [SWE-bench](https://github.com/SWE-bench/SWE-bench), with fresh working copies and independent upstream checks.

Both runs received the original report and this request:

> Fix the bug described in fixture/issue.txt. Work only in fixture.

The skill run added "Use BugDoctor." The upstream repair and evaluation tests were kept out of both working copies.

## Fix the cause of a matrix crash

The report described repeated multiplication of a block matrix containing zero blocks.

Baseline response excerpt:

> Block multiplication now preserves `ZeroMatrix` dimensions using matrix-aware addition.

BugDoctor response excerpt:

> Removed scalar-zero injection into matrix-only sums, preserving `ZeroMatrix` dimensions.

The baseline repaired block multiplication. Shared matrix addition still produced a scalar zero, losing the matrix's dimensions. BugDoctor repaired that earlier conversion.

| Independent checks | Baseline | BugDoctor |
| --- | --- | --- |
| Passed | 21 | 22 |
| Failed | 1 | 0 |
| Existing expected failure | 1 | 1 |

Source: [SymPy's upstream repair](https://github.com/sympy/sympy/pull/17630).

## Check related comparison methods

Another report described comparisons that failed to call an external object's reflected method.

Baseline fixed the basic equality path but left two number-comparison checks failing. BugDoctor fixed an additional comparison path: 96 checks passed instead of 95. One failure remained, so this was a partial repair.

Source: [SymPy's comparison repair](https://github.com/sympy/sympy/pull/13091).

Other tested cases tied. These selected examples establish specific gains, not an overall accuracy or speed advantage.
