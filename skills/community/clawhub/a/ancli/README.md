# ancli

Apple Notes CLI for macOS. List, search, read, create, append to, move and
delete notes from the command line, with `--json` for scripts. Notes has no
public framework, so ancli drives Notes.app through JXA scripting.

```bash
npm install -g @gopaljigaur/ancli
ancli setup                                  # grant Automation access once
ancli folders
ancli list --folder Notes --limit 10
ancli search "shopping" --json
ancli show p123                              # plain text; --html for the stored HTML
ancli create "Shopping list" "Milk" --folder Notes
echo "Eggs" | ancli append p123
ancli move p123 "Archive"
ancli delete p123                            # asks first; -y in scripts
```

## Ids

Notes identifies everything by a Core Data URL such as
`x-coredata://<store>/ICNote/p123`. ancli shows the short tail (`p123`) and
accepts either. If two accounts share a tail, ancli asks for the full URL,
which `--json` output carries as `url`.

## Folders

`--folder` takes a name, case-insensitive, or an id. When a name exists in
more than one account, write `Account/Folder`, for example `iCloud/Notes`.
`list` and `search` skip Recently Deleted unless you name it.

## Notes on behaviour

- `list` reads titles and dates only, never bodies, so it stays quick on large
  libraries. `search` lets Notes do the matching and fetches text only for the
  results it shows.
- Locked notes are listed with `locked: true`; their bodies cannot be read or
  appended to until they are unlocked in Notes.
- `create` and `append` read the text from stdin when it is piped or given as
  `-`. The first line of a note is its title.
- `append` refuses notes with attachments, because rewriting the body through
  scripting drops them.
- `delete` moves a note to Recently Deleted, where Notes keeps it for 30 days.
  Deleting it again from there removes it for good. Without a terminal it
  needs `--yes`.

## Permissions

The first command asks macOS whether your terminal may control Notes. If you
said no, turn it on in System Settings > Privacy & Security > Automation,
under your terminal app. If it is not listed, `tccutil reset AppleEvents`
makes macOS ask again.

Exit codes: `0` ok, `1` runtime error, `2` bad arguments, `10` not allowed to
control Notes.
