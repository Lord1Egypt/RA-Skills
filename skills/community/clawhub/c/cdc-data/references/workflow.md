# Workflow

```mermaid
stateDiagram-v2
  [*] --> Normalize
  Normalize --> Disambiguate: ambiguous query
  Normalize --> SelectAdapter: valid query
  SelectAdapter --> Browse
  Browse --> Verify
  Verify --> Return: locate
  Verify --> SavePDF: explicit download
  Verify --> TemporaryPDF: PDF extraction only
  Verify --> ExtractHTML: HTML extraction
  SavePDF --> ExtractPDF: extract also requested
  SavePDF --> Return: download only
  TemporaryPDF --> ExtractPDF
  ExtractPDF --> Vision: authorized and relevant pages
  ExtractPDF --> Return: native result
  Vision --> Return
  ExtractHTML --> Return
  Disambiguate --> [*]
  Return --> [*]
```

Start every query from the selected adapter. Browser state is task-local and is never persisted.

Use ordinary HTTP only after a concrete browser page-access failure. It must obey the same URL and content assertions and cannot expand adapter permissions.

Close named browser sessions and remove task-temporary PDFs and renders after success or failure. Cleanup failures become warnings and do not erase a successful result.
