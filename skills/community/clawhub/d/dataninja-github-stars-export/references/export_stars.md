# Export GitHub Stars Script

The `export_stars.sh` script is a powerful command-line utility that extracts all of your starred GitHub repositories, grouped neatly by their custom GitHub Lists (categories), and formats them into a Markdown table.

## Features

- **Category Grouping**: Organizes your stars directly into the Lists you created on GitHub.
- **Full Pagination Support**: Properly paginates through categories and repositories. Unlike a simple GraphQL query that caps at 100, this script correctly fetches an unlimited number of categories and items.
- **Markdown Ready**: Automatically generates a completely formatted Markdown file (`starred_lists.md`) ready to be viewed in any Markdown editor or uploaded to a repository.

## Requirements

To run this script, you will need the following dependencies installed on your system:

1. **[GitHub CLI (`gh`)](https://cli.github.com/)**: Standard command-line tool for GitHub.
   - You must be authenticated with the CLI and have the necessary scopes.
   - Run `gh auth status` to check if you are logged in.
   - If not, run `gh auth login` and follow the prompts.
2. **[jq](https://jqlang.github.io/jq/)**: A lightweight and flexible command-line JSON processor.
   - Mac: `brew install jq`
   - Debian/Ubuntu: `sudo apt-get install jq`
   - Arch Linux: `sudo pacman -S jq`

## Usage

1. Open your terminal.
2. Ensure the script is executable. If it isn't, run:
   ```bash
   chmod +x export_stars.sh
   ```
3. Execute the script:
   ```bash
   ./export_stars.sh
   ```

## Output Format

The script will write an output file called `starred_lists.md` in the current working directory. The output is structured with the category name as a header (level 2), followed by a Markdown table. 

### Columns Included
- **Repo name**: The name of the repository.
- **Repo handler**: The username or organization that owns the repository.
- **Full URL to Repo**: The direct link to the repository on GitHub.
- **Number of Stars**: The current total stargazer count for that repository.

### Output Example

```markdown
## 🤖 Machine Learning

| Repo name | Repo handler | Full URL to Repo | Number of Stars |
|---|---|---|---|
| cleanlab | cleanlab | https://github.com/cleanlab/cleanlab | 9324 |
| human-learn | koaning | https://github.com/koaning/human-learn | 1500 |
```

## How It Works Under The Hood

The script performs the following operations:

1. Uses the GitHub GraphQL API to fetch a complete, paginated list of all your custom List categories.
2. Uses `jq` to parse that list to extract the `id` and `name` strings natively.
3. Loops through each `id` to fire off targeted point GraphQL API queries specifically fetching the starred repositories tagged within that category. It fetches these via nested pagination to bypass standard GitHub API limits.
4. Directly injects the formatted output into an active Markdown file using Bash string interpolation and `jq` object mapping.
