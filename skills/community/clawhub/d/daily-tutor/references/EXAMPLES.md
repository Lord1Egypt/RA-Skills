# Data Format Examples

Below are a few examples for reference. Your `data.json` can follow **any structure** — these are not the only formats supported. The script will dynamically read all fields for you.

| Subject | Example fields |
|---------|---------------|
| Japanese | `word`, `reading`, `meaning`, `example` |
| English | `word`, `part_of_speech`, `meaning`, `example` |
| Mathematics| `formula`, `name`, `description`, `example` |
| History | `event`, `year`, `description`, `significance` |
| Chemistry | `element`, `symbol`, `atomic_number`, `properties` |
| Programming| `concept`, `language`, `syntax`, `explanation` |
| _Any Subject_| _Define any fields that fit your needs_ |

## Example: Japanese
```json
[
  {
    "word": "食べる",
    "reading": "taberu",
    "meaning": "to eat",
    "example": "りんごを食べる"
  }
]
```

## Example: Mathematics
```json
[
  {
    "formula": "E = mc^2",
    "name": "Mass–energy equivalence",
    "description": "Expresses the relationship between mass and energy."
  }
]
```
