# Running The Review's Own Checks

The commands a Rails review should run before it reports a verdict.

## The change and its callers

```bash
# the change
git diff main...HEAD --stat
git diff main...HEAD --name-only

# who depends on it
grep -rn "<changed_method>" --include="*.rb" app/ lib/
```

A file you cannot list the callers of is a file you have not reviewed.

## The tests

```bash
bundle exec rspec spec/models spec/requests
```

Run the specs the change touches. If the change has no spec coverage, that is
a finding in itself - the review of an untested change is a code read.

## RuboCop, scoped

```bash
bundle exec rubocop -A app/ spec/
git diff spec/   # read what it changed
```

**Always scope the path.** A bare `rubocop -A` walks the whole tree including
vendored and generated code, and can autocorrect files you do not own.

**Read the diff before accepting it.** The `Style/NumericPredicate` cop
rewrites `be.positive?` to `be_positive`, which is a `NoMethodError` at
runtime, not a style fix. And `-A` (unsafe autocorrect) can rewrite a spec's
structure - never accept an autocorrect that changed the number of
expectations in a test.

## Verify the thing you are about to claim

Before reporting a bug as fixed, run the exact surface that failed. A change
that was never exercised against the original failure is an unverified change.

```bash
bundle exec rspec spec/paths/to/the/failing_spec.rb
```

Do not report green without running the specific check that was red.

## Related

- `adversarial-code-review` - the main skill
- `rails-tdd-standards` - RSpec standards and spec gotchas
- `rails-ci-fixer` - CI-only failure patterns
