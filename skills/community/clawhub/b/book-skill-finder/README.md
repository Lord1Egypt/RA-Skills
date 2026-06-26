# find-book

Local book search skill. Search 5904 nonfiction books from Heardly database.

## Installation

```bash
clawhub install find-book
```

## Usage

```javascript
const FindBookSkill = require('find-book');
const skill = new FindBookSkill();

// Search by title or author
const result = skill.search('Atomic Habits');

// Result format:
{
  found: true,
  results: [
    {
      title: 'Atomic Habits',
      author: 'James Clear',
      rating: 9.5,
      summary: '...',
      image: 'https://...',
      heardly_link: 'https://heardly.app/book/...',
      suggested_additions: {
        SOUL: '...',
        MEMORY: '...',
        SKILL: '...'
      }
    }
  ]
}
```

## API

### search(query, maxResults = 5)
Search books by title or author name.

### getByTitle(title)
Get exact book by title.

## Data

- 5904 nonfiction books
- Local JSON cache (no network calls)
- Heardly curated collection
- English language

## License

MIT
