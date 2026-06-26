---
name: emacs-control
description: Control Emacs. Search, edit, navigate, and pair programming with user
---

# Emacs Control Skill

Use `emacsctl` to interact with running Emacs.

## CLI Usage

```
emacsctl [options]... [arguments]...

Options:
  -i, --insert                Perform insertion
  -r, --replace               Perform replacement
  -b, --buffer BUFFER         Buffer for insertion or replacement. Current buffer by default
  -s, --save                  Save the buffer after insertion or replacement
  -p, --position INSERT_POSITION
  -l, --line INSERT_LINE
  -c, --column INSERT_COLUMN
      --start-position REPLACE_START_POSITION
      --end-position REPLACE_END_POSITION
      --start-line REPLACE_START_LINE
      --end-line REPLACE_END_LINE
  -h, --help
```

*`emacsctl` needs configure for both agent and Emacs side. Check https://github.com/calsys456/emacsctl for proper setup and notice user if possible when `emacsctl` not found or returned connection failure*

### Eval

Basically, `emacsctl` retrieve a string of S-expressions, either from first argument or `stdin`, then `read` and `eval` them with `progn` inside Emacs, and print the return value of the last expression.

```bash
emacsctl '(emacs-version)'
# with pipe
echo '(emacs-version)' | emacsctl 
# => "GNU Emacs XX.X.XX"

# Use HEREDOC for multi-line input or input with quote
# Note that HEREDOC has trailing newline
emacsctl <<EOF
(defun multi-line-function ()
  (message "Hello my user")
  'return-to-me)
(multi-line-function)
EOF
# => return-to-me
```

*Be careful with interactive or blocking functions (like read-string, y-or-n-p) as they will hang.*

*When mistake happened, suggest user to undo or revert. only undo in yourself (e.g. `emacsctl '(undo)'`) if nothing important or you are confident to do so.*

**BE CAREFUL WHEN EVAL**

### Insert

When `-i` specified, `emacsctl` will perform insertion with given string, file or `stdin`:

```bash
# Insert "Hello" at line 50, column 15 of buffer emacsctl.el
emacsctl -i -b "emacsctl.el" -l 50 -c 15 -p 100 "Hello"

# Insert your-code at point 100 of current buffer
emacsctl -i -p 100 <<EOF
<your-code>
EOF

# Insert the content of ~/gpl-3.0.txt at the current point of current buffer, and save the buffer
emacsctl -i -s ~/gpl-3.0.txt
```

### Replace

When `-r` specified, `emacsctl` can perform buffer content replacement in two style: replacing range or replacing certain text.

#### Replacing Range

Specify `--start-position` and `--end-position`, or `--start-line` and `--end-line` to replace a range:

```bash
# Replace first 5 characters of buffer emacsctl.el with "XXXXX"
emacsctl -r -b "emacsctl.el" --start-position 1 --end-position 5 "XXXXX"

# Replace line 50-100 of the current buffer with your-code, and save the buffer
emacsctl -r --start-line 50 --end-line 100 -s <<EOF
<your-code>
EOF
```

#### Replacing Certain Text

Give 2 strings or files, to replace the first (old-text) to second (new-text):

```bash
# Replace nearest "(require 'function)" form of buffer emacsctl.el to the content of ~/function.el
emacsctl -r -b "emacsctl.el" "(require 'function)" ~/function.el

# Replace `to-be-refined` function to `refined` function in current buffer
emacsctl -r <(cat <<OLD_TEXT
(defun to-be-refined ()
  (message "replace me"))
OLD_TEXT
) <<NEW_TEXT
(defun refined ()
  (message "new message"))
NEW_TEXT
```

If there's multiple occurrence of old-text, only the one nearest from current point will be replaced. For bulk replacement or regex-based replacement, write ELisp instead.

## Interface

Here is some specially designed ELisp functions for agent use, start with `emacsctl-` and return informative Lisp plist. Call them with `Eval` if possible.

### Point and Mark

Use `(emacsctl-point-info &optional (surrounding 2))` and `(emacsctl-mark-info &optional (surrounding 2))` for information and surrounding contents for point and mark.

The current point is marked out using "█" and current mark is using "▄".

### Buffer

Use `(emacsctl-buffer-info &optional (buffer (current-buffer)))` for buffer state and metadata.

Use `(emacsctl-buffer-imenu &optional (buffer (current-buffer)))` for buffer overview.

Fuzzy-match normal buffers using `(emacsctl-buffer-list &optional match)`. Use `(emacsctl-hidden-buffer-list &optional match)` similarly for hidden buffers.

#### Grep Buffer

Use `(emacsctl-grep pattern &optional (buffer (current-buffer)))` to grep buffer content. It will return match result and surroundings.

Use Emacs-specific regular expression. Try to construct regex with `rx` or `regexp-*` functions if there's difficult.

#### Read Buffer

Function:
`(emacsctl-read-buffer &key (buffer (current-buffer)) 
                            line (start-line line) (end-line line)
                            position (start-position (or position (point-min))) (end-position (or position (point-max)))
                            (surrounding 2)
                            full-p)`

Examples:

```elisp
;; Read a region
(emacsctl-read-buffer :start-position <point-number> :end-position <point-number>)
;; Read lines
(emacsctl-read-buffer :start-line <line-number> :end-line <line-number>)
;; Get region around line
(emacsctl-read-buffer :line <line-number> :surrounding 20)
;; Retrieve FULL content of the buffer (USE WITH CAUTION)
(emacsctl-read-buffer :buffer <buffer> :full-p t)
```

### Window

Use `(emacsctl-query-window)` to view the window layout of current frame. Use `(emacsctl-select-window <index>)` to switch to a window using the index returned by query.

### Kill Ring (Pasteboard)

Use `(emacsctl-query-kill-ring)` for a brief view of the kill-ring. Write ELisp code to search in-detail.

### Environment Inquiries

To search symbol, use `(emacsctl-search-symbol <pattern>)`; For command, use `(emacsctl-search-command <pattern>)`; For function, use `(emacsctl-search-function <pattern>)`; For variable, use `(emacsctl-search-variable <pattern>)`. They will return useful informations.

Pattern will be breaked down by dashes and matched in substring. Accurate query will get better detail.

## Tips

The emacs-control skill is not for replacing other tool calls. Emacs is for bodied humans but not you. **Use other file-based tools for efficient work, and `emacsctl` only if it is really needed or user asked to.**
