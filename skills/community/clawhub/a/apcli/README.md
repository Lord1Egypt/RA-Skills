# apcli

Apple Contacts CLI for macOS. Search, read, create, update and delete contacts
from the command line, with `--json` for scripts. Uses the Contacts framework
through JXA, so Contacts.app never has to open.

```bash
npm install -g @gopaljigaur/apcli
apcli setup                     # grant Contacts access once
apcli search ana --json
apcli contact <id>
apcli create --given Ana --phone mobile:+491701234567 --email ana@example.com
apcli update <id> --social telegram:@ana --remove-phone +491701234567
apcli delete <id>               # asks first; --yes in scripts
```

Social profiles hold handles for services Contacts has no field for:
`--social telegram:@ana`, `--social discord:<user id>`.

Exit codes: `0` ok, `1` runtime error, `2` bad arguments, `10` Contacts access
not granted.
