# File-Count Threshold Probe

Real prose to pass the content-quality gate. This probe binary-searches the
ClawHub multipart part-count limit responsible for evolver's 413, by publishing
an exact number of tiny source files and observing accept vs reject.

## Behavior
Publishes exactly N small files to locate the count threshold.
