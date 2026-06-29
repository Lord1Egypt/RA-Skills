## BCMS Permissions

BCMS permissions control what users and API keys can do.

### User permissions

- Users can be granted broad roles or granular rights.
- Only admins should be allowed to create/modify templates, widgets, groups and API keys.

### API key permissions

- Permissions can be configured in **simple** or **advanced** modes.
- In advanced mode you can specify per‑resource rights:

  - `get`
  - `create`
  - `update`
  - `delete`

- Keys can be scoped per template, function and sometimes media operations.

### Least‑privilege design

- Create **separate keys** for:

  - Public, read‑only content delivery.
  - Internal management tools (may need create/update/delete).
  - Media delivery or uploads.
  - Function invocation.

- Regularly review and rotate keys, revoking those that are no longer needed.

When the agent encounters permission errors, it should:

1. Check that the correct key is being used for the environment.
2. Verify that the key has the necessary scopes for the operation.
3. Consult organisation administrators if broader rights are required.
