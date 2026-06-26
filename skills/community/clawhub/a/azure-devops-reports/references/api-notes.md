# API Notes

## Minimum PAT scopes

For this read-only reporting skill, start with:

- Work Items Read (`vso.work`)
- Project and Team Read (`vso.project`)

Add more scopes only if you extend the skill later.

## Endpoint patterns

- Projects: `GET https://dev.azure.com/{org}/_apis/projects?api-version=7.1`
- Teams in project: `GET https://dev.azure.com/{org}/_apis/projects/{project}/teams?api-version=7.1-preview.3`
- Team members: `GET https://dev.azure.com/{org}/_apis/projects/{project}/teams/{team}/members?api-version=7.1-preview.1`
- Team iterations: `GET https://dev.azure.com/{org}/{project}/{team}/_apis/work/teamsettings/iterations?api-version=7.1-preview.1`
- Team current iteration: `GET https://dev.azure.com/{org}/{project}/{team}/_apis/work/teamsettings/iterations?$timeframe=current&api-version=7.1-preview.1`
- Project WIQL: `POST https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.1`
- Team WIQL: `POST https://dev.azure.com/{org}/{project}/{team}/_apis/wit/wiql?api-version=7.1`
- Work items batch: `POST https://dev.azure.com/{org}/_apis/wit/workitemsbatch?api-version=7.1` (Limit: 200 IDs per request. Implementation chunks larger lists into batches of 200).
- Query by ID: `GET https://dev.azure.com/{org}/{project}/_apis/wit/wiql/{queryId}?api-version=7.1` (Returns list of IDs, which must then be fetched via batch).

## Auth

Use Basic auth with empty username and PAT as password.

`Authorization: Basic base64(':' + PAT)`

Never print this header.
