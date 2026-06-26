# bioRxiv API Documentation

BioRxiv API base URL: `https://api.biorxiv.org`

## Endpoints

### Get Collection Details
- `GET /details/bioinformatics/<interval>/<cursor>`
- `<interval>`: Date range like "2026-03-01/2026-03-09"
- `<cursor>`: Starting position (0-indexed), default 0
- Returns: JSON with collection of papers

### Response Format
```json
{
  "collection": [
    {
      "doi": "10.1101/2026.03.01.123456",
      "title": "Paper Title",
      "authors": ["Author1", "Author2"],
      "author_corresponding": "Author1",
      "author_corresponding_institution": "University",
      "date": "2026-03-01",
      "version": "1",
      "type": "new"
    }
  ],
  "messages": [],
  "total": 100
}
```

## Available Collections
- bioinformatics
- genomics
- molecular-biology
- cell-biology
- genetics
- evolutionary-biology
- ecology
- neuroscience
- plant-biology
- microbiology
- immunology
- cancer-biology
- biochemistry
- biophysics
- structural-biology
- systems-biology
- synthetic-biology
- developmental-biology
- computational-biology

## Python Script Usage

```python
import requests

def get_papers(collection="bioinformatics", start_date="2026-03-01", end_date="2026-03-09", cursor=0):
    url = f"https://api.biorxiv.org/details/{collection}/{start_date}/{end_date}/{cursor}"
    resp = requests.get(url)
    return resp.json()
```
