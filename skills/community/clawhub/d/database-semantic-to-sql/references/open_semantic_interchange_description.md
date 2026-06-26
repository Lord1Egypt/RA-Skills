# Open Semantic Interchange (OSI) - Field Specification

## 1. Introduction

This document provides a comprehensive field specification for the Open Semantic Interchange (OSI) YAML configuration file. The semantic model defines the structure for domain-specific data queries and analysis across various business contexts.

The YAML file serves as a metadata layer that enables AI-powered query generation and data interpretation for structured datasets.

## 2. Document Structure

This specification is organized hierarchically to mirror the YAML file structure:

- **Top-Level Fields**: Global configuration fields
- **Semantic Model**: Theme-level definitions
- **Datasets**: Individual data source definitions
- **Fields**: Detailed field specifications within each dataset

## 3. Top-Level Fields

### 3.1 `yaml-language-server`

**Data Type**: Comment directive

**Description**: Specifies the JSON schema path for YAML language server validation and IDE auto-completion support.

**Format**: `$schema=<path-to-schema>`

**Constraints**: Must reference a valid schema file path relative to the YAML file location.

---

### 3.2 `version`

**Data Type**: String

**Description**: Defines the semantic model version number using semantic versioning convention.

**Format**: `MAJOR.MINOR.PATCH`

**Constraints**: 
- Must follow semantic versioning format
- Each component must be a non-negative integer

**Default Value**: `0.0.1`

---

### 3.3 `semantic_model`

**Data Type**: Object

**Description**: The semantic model definition. In the current generator implementation, this file contains exactly one semantic model object.

**Required Sub-fields**:
- `name`
- `description`
- `ai_context`
- `datasets`
- `relationships`
- `metrics`
- `terms`
- `rules`

---

## 4. Semantic Model Object

### 4.1 `name`

**Data Type**: String

**Description**: The theme name that identifies the semantic model's thematic classification.

**Constraints**: 
- Must be a non-empty string
- Should be unique within the system

---

### 4.2 `description`

**Data Type**: String

**Description**: A brief description explaining the semantic model's purpose and scope.

**Constraints**: 
- Must be a non-empty string
- Should clearly describe the theme's domain

---

### 4.3 `ai_context`

**Data Type**: Object

**Description**: AI context configuration containing instruction information for AI processing.

#### 4.3.1 `instructions`

**Data Type**: String

**Description**: AI processing instructions that guide the AI on how to utilize this semantic model for data queries and analysis.

**Constraints**: 
- Must be a non-empty string
- Should provide clear guidance on the model's usage

---

### 4.4 `datasets`

**Data Type**: Array of objects

**Description**: List of datasets, where each dataset corresponds to a database table or view.

**Required Sub-fields** (for each dataset):
- `name`
- `source`
- `description`
- `ai_context`
- `fields`

---

### 4.5 `relationships`

**Data Type**: Array of objects

**Description**: Relationship definitions derived from foreign keys (table-to-table joins).

**Default Value**: `[]`

**Required Sub-fields** (for each relationship):
- `name`
- `from_table`
- `to_table`
- `from_columns`
- `to_columns`

---

### 4.6 `metrics`

**Data Type**: Array of objects

**Description**: Reserved for metric definitions (not populated by the current generator, but present in the output schema).

**Default Value**: `[]`

---

### 4.7 `terms`

**Data Type**: Array of objects

**Description**: Reserved for terminology definitions (not populated by the current generator, but present in the output schema).

**Default Value**: `[]`

---

### 4.8 `rules`

**Data Type**: Array of objects

**Description**: Reserved for rule definitions (not populated by the current generator, but present in the output schema).

**Default Value**: `[]`

---

## 5. Dataset Object

### 5.1 `name`

**Data Type**: String

**Description**: Dataset identifier that should correspond to the database table name.

**Constraints**: 
- Must use snake_case naming convention
- Must be unique within the semantic model
- Should match the actual database table name

---

### 5.2 `source`

**Data Type**: String

**Description**: Complete data source path specifying the database and table location.

**Format**: `database_name.table_name`

**Constraints**: 
- Must follow the format `<database>.<table>`
- Both database and table names must be valid identifiers

---

### 5.3 `description`

**Data Type**: String

**Description**: Dataset description explaining the dataset's purpose or content.

**Constraints**: 
- Must be a non-empty string
- Should briefly describe what the dataset contains

---

### 5.4 `ai_context`

**Data Type**: Object

**Description**: AI context configuration for the dataset.

#### 5.4.1 `ai_name`

**Data Type**: String

**Description**: AI-recognized name for the dataset, used for natural language query processing.

**Constraints**: 
- Must be a non-empty string
- Should be consistent with the dataset name or description

---

#### 5.4.2 `weight`

**Data Type**: Integer

**Description**: Dataset weight for ranking/recall bias during matching. Higher value means the dataset is more likely to be selected.

**Default Value**: `3`

---

#### 5.4.3 `synonyms`

**Data Type**: Array of strings

**Description**: Alternative dataset names used for matching.

**Default Value**: `[]`

---

#### 5.4.4 `default_datetime_field`

**Data Type**: String

**Description**: The default time field name for the dataset, selected by the generator by scoring date/time columns. This replaces the need for a field-level `is_default` flag in the current YAML output.

**Default Value**: `` (empty string)

**Constraints**:
- If provided, it should match one of the dataset `fields[*].name`

---

### 5.5 `fields`

**Data Type**: Array of objects

**Description**: List of field definitions for the dataset. Each field represents a column in the database table.

---

## 6. Field Object

### 6.1 `name`

**Data Type**: String

**Description**: Field identifier that must match the database column name.

**Constraints**: 
- Must use snake_case naming convention
- Must exactly match the database column name
- Must be unique within the dataset

---

### 6.2 `type`

**Data Type**: String

**Description**: Field data type that determines query methods and presentation format.

**Allowed Values**:

| Value | Description | Usage |
|-------|-------------|-------|
| `TEXT` | Text/string data | Names, codes, descriptions |
| `NUMBER` | Numeric data | Counts, measurements, amounts |
| `DATE` | Date data | Date-only values |
| `TIME` | Time/date-time data | Timestamps, datetime |
| `ID` | Identifier | UUID/GUID-like identifiers |
| `OTHER` | Other types | Fallback when type is not recognized |

**Constraints**: 
- Must be one of the allowed values
- Must match the actual database column data type

---

### 6.3 `description`

**Data Type**: String

**Description**: Human-readable field description used for UI display and documentation.

**Constraints**: 
- Must be a non-empty string
- Should clearly describe the field's meaning
- Typically written in the local language for the target domain

---

### 6.4 `ai_context`

**Data Type**: Object

**Description**: Field-level AI context configuration containing metadata for AI processing.

**Common Sub-fields**:
- `ai_name`
- `property`
- `ai_type` (optional)
- `value_list` (optional, for enum)

#### 6.4.1 `ai_name`

**Data Type**: String

**Description**: AI-recognized field name, typically identical to the `description` field.

**Constraints**: 
- Must be a non-empty string
- Should match or be similar to the `description` value

---

#### 6.4.2 `property`

**Data Type**: String

**Description**: Field property type that indicates special field attributes.

**Allowed Values**:

| Value | Description | Usage Scenario |
|-------|-------------|----------------|
| `normal` | Normal field | Standard data fields |
| `dimension` | Dimension field | Used for grouping/filtering, e.g. date/time dimensions or enum dimensions |
| `detail_only` | Detail query only | Fields displayed only in detail queries, not used in aggregations |

**Default Value**: `normal`

**Constraints**: 
- Must be one of the allowed values

---

#### 6.4.3 `ai_type`

**Data Type**: String

**Description**: AI field type indicator for special processing requirements.

**Allowed Values**:

| Value | Description | Usage Scenario |
|-------|-------------|----------------|
| `date` | Date type | Reserved for date-specific processing (not always emitted by the current generator) |
| `enum` | Enumeration type | Fields with fixed allowable values (emitted when enum is detected) |

**Default Value**: `` (empty string)

**Constraints**: 
- Must be one of the allowed values
- If `enum`, then `value_list` must be provided

---

#### 6.4.4 `value_list`

**Data Type**: Array of scalars (strings and/or numbers)

**Description**: List of allowable values for enumeration-type fields.

**Usage**: 
- Required when `ai_type` is `enum`
- Should be omitted or empty for non-enumeration fields

**Constraints**: 
- Must be an array (can be empty)
- For enumeration fields, must contain all valid values (as extracted from samples / metadata)

---

## 7. Relationship Object

Relationship entries live under `semantic_model.relationships`.

### 7.1 `name`

**Data Type**: String

**Description**: Human-readable relationship name. The generator uses the form `<from_table> to <to_table>`.

---

### 7.2 `from_table`

**Data Type**: String

**Description**: Source table for the relationship.

---

### 7.3 `to_table`

**Data Type**: String

**Description**: Target table for the relationship.

---

### 7.4 `from_columns`

**Data Type**: Array of strings

**Description**: Column list on `from_table` participating in the join.

---

### 7.5 `to_columns`

**Data Type**: Array of strings

**Description**: Column list on `to_table` participating in the join. It should align positionally with `from_columns`.

---

## 8. Numeric Format (`num_format`) Object

`num_format` is an optional object on a field, emitted when the generator detects unit/level/decimal hints.

### 8.1 `unit`

**Data Type**: String

**Description**: Display unit hint (e.g. 元, 万, %, etc.).

---

### 8.2 `num_level`

**Data Type**: String

**Description**: Numeric magnitude/level hint (e.g. 千/万/亿) used for formatting.

---

### 8.3 `num_decimal`

**Data Type**: String or Integer

**Description**: Decimal precision hint for formatting.
