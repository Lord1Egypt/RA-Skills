#!/bin/bash

# Define the output file name
OUTPUT_FILE="assets/starred_lists.md"

echo "Fetching starred repositories organized by category (supports >100 lists and >100 stars per list)..."

> "$OUTPUT_FILE"

# 1. Fetch all lists first (handling pagination via gh api --paginate)
echo "Fetching all categories..."
LISTS_JSON=$(gh api graphql --paginate -f query='
query($endCursor: String) {
  viewer {
    lists(first: 100, after: $endCursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id
        name
      }
    }
  }
}' --jq '.data.viewer.lists.nodes[]' 2>/dev/null)

if [ -z "$LISTS_JSON" ]; then
    echo "No lists found or an error occurred."
    exit 1
fi

# 2. Iterate over the lists and fetch items for each one
echo "$LISTS_JSON" | jq -c '.' | while read -r list; do
  list_id=$(echo "$list" | jq -r '.id')
  list_name=$(echo "$list" | jq -r '.name')
  
  echo "Processing category: $list_name..."
  
  echo "## $list_name" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo "| Repo name | Repo handler | Full URL to Repo | Number of Stars |" >> "$OUTPUT_FILE"
  echo "|---|---|---|---|" >> "$OUTPUT_FILE"

  # Fetch paginated items for this specific list
  # Note: The '?' allows jq to handle cases where items might be empty without erroring out
  gh api graphql --paginate -F id="$list_id" -f query='
query($id: ID!, $endCursor: String) {
  node(id: $id) {
    ... on UserList {
      items(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          ... on Repository {
            name
            owner { login }
            url
            stargazerCount
          }
        }
      }
    }
  }
}' --jq '.data.node.items.nodes[]? | select(. != null) | "| \(.name) | \(.owner.login) | \(.url) | \(.stargazerCount) |"' >> "$OUTPUT_FILE"
  
  echo "" >> "$OUTPUT_FILE"
done

echo "Successfully saved all repositories to $OUTPUT_FILE"
