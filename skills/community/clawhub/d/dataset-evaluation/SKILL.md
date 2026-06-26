# SKILL.md --- dataset_evaluation

## Skill Name

`dataset_evaluation`

## Description

Evaluate a miner submission by performing two evaluation steps:

1.  **Content Consistency Evaluation**
2.  **Structured Data Quality Evaluation**

The evaluator receives **5 cleaned data samples**, the **structured
JSON**, and the **dataset schema**, then computes a final score for the
miner.

------------------------------------------------------------------------

# Input

``` json
{
  "cleaned_data_list": [
    "cleaned_text_1",
    "cleaned_text_2",
    "cleaned_text_3",
    "cleaned_text_4",
    "cleaned_text_5"
  ],
  "structured_data": {
    "field1": "value",
    "field2": "value"
  },
  "dataset_schema": {
    "fields": [
      {"name": "title", "type": "string", "required": true},
      {"name": "author", "type": "string", "required": false},
      {"name": "date", "type": "string", "required": false},
      {"name": "url", "type": "string", "required": true}
    ]
  }
}
```

------------------------------------------------------------------------

# Evaluation Procedure

## Step 1 --- Content Consistency Evaluation (Weight 40%)

Goal: determine whether the **5 cleaned texts represent the same
underlying content**.

### Method

1.  Normalize text

-   remove HTML
-   lowercase
-   remove excessive whitespace

2.  Compute pairwise similarity across the 5 texts

Recommended metrics:

-   cosine similarity (embedding based)
-   OR Jaccard similarity

3.  Compute the **average similarity score**.

### Output

    content_consistency_score (0-100)

Suggested mapping:

    avg_similarity >= 0.9 → 100
    0.8 – 0.9 → 80 – 100
    0.6 – 0.8 → 60 – 80
    0.4 – 0.6 → 40 – 60
    < 0.4 → < 40

------------------------------------------------------------------------

# Step 2 --- Structured Data Quality Evaluation (Weight 60%)

Using the **verified cleaned content**, evaluate the **structured
JSON**.

Compute four sub-scores.

------------------------------------------------------------------------

## 2.1 Field Completeness (30%)

Evaluate whether all **required fields** exist.

Formula:

    completeness_score =
        (# required fields present / total required fields) * 100

------------------------------------------------------------------------

## 2.2 Value Accuracy (40%)

Evaluate whether each field value is **consistent with the cleaned
data**.

Examples:

-   title appears in cleaned text
-   author name appears in text
-   url matches source

Scoring guideline:

    exact match → 100
    partially correct → 60-80
    inconsistent → <50

------------------------------------------------------------------------

## 2.3 Type Correctness (15%)

Evaluate whether values match schema types.

Examples:

    string
    number
    boolean
    array

Formula:

    type_score =
        (# correct types / total fields) * 100

------------------------------------------------------------------------

## 2.4 Information Sufficiency (15%)

Evaluate whether the structured data **misses obvious information**
present in the cleaned text.

Example:

Cleaned text contains:

    title
    author
    date

But structured JSON only includes:

    title

Then deduct score.

Guideline:

    complete extraction → 100
    minor missing info → 70–90
    major missing info → <60

------------------------------------------------------------------------

# Structuring Quality Score

    structuring_quality_score =
        completeness_score * 0.30
      + value_accuracy_score * 0.40
      + type_score * 0.15
      + information_sufficiency_score * 0.15

Range:

    0 – 100

------------------------------------------------------------------------

# Step 3 --- Final Miner Score

    miner_score =
        content_consistency_score * 0.4
      + structuring_quality_score * 0.6

Range:

    0 – 100

------------------------------------------------------------------------

# Output Format

The evaluator must return:

``` json
{
  "content_consistency_score": 92,
  "structuring_quality_score": 85,
  "miner_score": 88.2,
  "details": {
    "completeness_score": 90,
    "value_accuracy_score": 88,
    "type_score": 100,
    "information_sufficiency_score": 80
  }
}
```

------------------------------------------------------------------------

# Evaluator Rules

The evaluator **must follow these principles**:

1.  Be deterministic and reproducible
2.  Base judgments only on provided inputs
3.  Avoid hallucination
4.  Penalize missing or inconsistent data
5.  Return scores strictly in the 0--100 range
