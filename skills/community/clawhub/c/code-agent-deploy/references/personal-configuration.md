# Parameters and secrets of a personal project

## How the product works

Every project has one owner; one platform can host the personal projects of many users. The owner manages their own deployments, logs and parameters. There are no teams, no collaborators, no approval flows, and no separate people in charge of test and production configuration. A project has one set of live configuration, with no environments. The owner is the developer whose deploy key created the project.

The normal course is: one deployment brings along the runtime parameters the project declares, and from then on the platform's parameters are reused. The parameters page is only a place to look and to change something by hand, not a step every deployment goes through.

## The first deployment

1. The skill works out which runtime parameters the project really needs and, as in "Two kinds of parameter whose value differs between local and live" below, where each one's value comes from (a local file, created by the platform, or typed by the user). Secret values are never printed.
2. The permission to deploy covers submitting the runtime parameters the project declares and the user selected; when source and fields are clear, no further approval is needed. Machine-wide credentials that were not named, files of other projects and unrelated secrets are out of scope.
3. Values are read from the local configuration that was explicitly chosen, and appcli submits them to the platform, which stores them encrypted. Parameters do not go into the image, into the image archive, or into the manifest in plain text.
4. The platform's reserved variables (PORT, HOSTNAME, PUBLIC_URL, DATABASE_URL, UPLOAD_DIR, GENERATED_DIR, and the database service's connection variables) are injected by the platform as described in section 2.2 of the [appcli reference](appcli-reference.md); user parameters cannot declare them. Every deployment starts with the parameter version bound to it.
5. When a deployment is created, the platform checks the required entries against the env declarations in the spec; when some are missing it returns `CONFIG_MISSING_REQUIRED` with the list.
6. Only when a required value is missing, or a local value does not suit the server, is the owner asked to supply it. That can be done locally or on the platform's parameters page; nobody is forced to the web page.

Do not upload .env.local blindly as a whole file. Submit only the declared business runtime parameters; leave out registry credentials, deploy keys and tokens, private keys and other projects' variables. A dotenv file is parsed as data and is never executed with `source`.

localhost addresses, absolute paths on the development machine and local callback URLs usually do not work live. Point them out when found and handle them by what the project or the platform really uses; never guess a server address.

## Two kinds of parameter whose value differs between local and live

A value used in local development is not necessarily right for a live environment that other people use. On the first submission, tell them apart by this table:

| Kind | Examples | Where the live value comes from | In the manifest |
|---|---|---|---|
| A signing secret the application uses for itself | SESSION_SECRET, JWT_SECRET, NEXTAUTH_SECRET, AUTH_SECRET, COOKIE_SECRET | The platform creates a new random value; the local value is not carried over | `generate` |
| A key that decrypts data already stored | ENCRYPTION_KEY, a data encryption key | When local data is migrated the local value must be kept, or the old data cannot be decrypted; without migrating data it can be `generate` | With migrated data, `source` pointing at the local file; otherwise `generate` |
| Credentials of a third-party service | OPENAI_API_KEY, payment keys, SMS / email service keys, an OAuth client secret | The user decides: keep the local value, or use credentials made for live use | Keep: `source`; different ones: `manual` |
| Ordinary configuration | A third-party service's address, feature switches | The local value; when it is localhost or a local path, ask for the live value | `source` |

Rules:

- Signing secrets are created by the platform by default: the local value may already have appeared in the repository, in screenshots or in chat logs. A new value live only invalidates old sessions, which does not matter on a first launch. The created value never passes through the developer's computer or the AI in plain, and is not shown on any page.
- Before third-party credentials are submitted for the first time, the user must be asked: "Are these credentials for development and testing? Once the application is live, other people using it will spend this account's quota or cost money." When the user chooses different credentials, mark them `manual` and ask the user to run `appcli config set <NAME>` in their own terminal; the plain value does not pass through the AI.
- When it cannot be told which kind a variable is, treat it as third-party credentials and ask the user.
- Rotating a signing secret: `appcli config regenerate <NAME>` followed by `appcli config apply` signs every signed-in user out; tell the user before doing it. A key that decrypts data cannot be rotated, or the old data can no longer be decrypted.

## Later deployments and changes on the page

- A value the platform already has comes first; an ordinary deployment only adds declared parameters that are new and missing, and never overwrites a value.
- Removing a variable locally does not remove the platform's value. Only when the user explicitly asks to carry the change or the removal over is that field updated.
- The owner gets a one-time sign-in link with `appcli console` and reaches the parameters page without a separate password. `appcli config get / set / unset / apply` work as well.
- The platform's page shows the parameter's name, an ordinary value, whether it is sensitive, and a way to edit it. Sensitive values are masked by default; leaving the field blank keeps the value, and setting an empty value and deleting are two distinct actions.
- On the page the owner can "save" or "save and apply". Saving restarts nothing; saving and applying recreates the container and health-checks it, and puts the old configuration back when that fails. The image is not rebuilt.
- The saved version and the running version are both shown; when applying fails, the state and the logs stay clear. Never report a successful save as being live.
- Public build-time variables (NEXT_PUBLIC_* and the like) are not runtime parameters and are not managed on the parameters page: they are declared in the manifest's buildEnv and passed in by appcli at build time, and a change needs a new deployment. A secret never goes into buildEnv.

## Limits that apply

- `appcli config get` returns the saved version, the running version, each parameter's attributes and whether it is set; it never returns a sensitive value in plain.
- An ordinary deployment writes only parameters the platform does not have yet and overwrites nothing. `appcli config set / unset / regenerate` change the current version; when someone else changed it in the meantime, `CONFIG_CONFLICT` is returned: read again and then change. Nothing is overwritten silently.
- `appcli config apply` makes the saved parameters live. When the project has no running version it returns `APPLICATION_NOT_RUNNING`, and the saved parameters are used by the next deployment. Each deployment records the parameter version it used.
- Sensitive values in logs are replaced by the platform, going by the project's current sensitive parameter values.
- Only the developer the project belongs to can read and change its parameters. Sensitive values are stored encrypted on the platform.
- A variable name matches `^[A-Z_][A-Z0-9_]{0,63}$`; a value has no NUL, is at most 16 KB, and all values together at most 64 KB. Parameters are not written into the image, and deployment logs record only parameter names and versions.

What can be relied on: a first deployment that brings its declared parameters starts; a second deployment keeps the values edited on the platform; a new required entry that is missing is reported; another account has no access; logs and the image contain no secrets; the saved and the applied versions are exact; changing a public build-time parameter calls for a new build.
