#!/usr/bin/env python3
"""
fill_xfa.py — Generic CLI tool to inspect and fill XFA (Adobe LiveCycle) PDF forms.

XFA forms store data as XML embedded in the PDF (AcroForm.XFA array, "datasets" packet).
Standard tools like pdftk do NOT work with XFA. This script manipulates the XML directly.

Usage:
    python3 fill_xfa.py fields form.pdf
    python3 fill_xfa.py fill form.pdf -o out.pdf --set Name=Wert --set Vorname=Max
    python3 fill_xfa.py fill form.pdf -o out.pdf -d data.json
    echo '{"Name":"Wert"}' | python3 fill_xfa.py fill form.pdf -o out.pdf --stdin

Requires: pikepdf >= 10.0
"""

import argparse
import collections
import json
import re
import sys
import xml.etree.ElementTree as ET

try:
    import pikepdf
except ImportError:
    sys.exit("Error: pikepdf is required. Install with: pip install pikepdf")


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def strip_namespaces(xml_text: str) -> str:
    """Remove all XML namespace declarations and prefixes so ElementTree can parse easily.

    Only operates on actual XML tags (not text/CDATA content) by requiring
    that the prefix:tagname is followed by a space, /, or >.
    """
    # Remove xmlns attributes (xmlns="..." and xmlns:prefix="...")
    xml_text = re.sub(r'\s+xmlns(?::\w+)?="[^"]*"', '', xml_text)
    # Remove namespace prefix from tag names only — require that the tag
    # is followed by whitespace, '/', or '>' so we don't match inside text content
    xml_text = re.sub(r'<(/?)\w+:(\w+)(?=\s|/?>)', r'<\1\2', xml_text)
    return xml_text


def find_leaf_fields(root: ET.Element) -> list[str]:
    """Return all leaf-element names (elements with no child elements, including empty ones)."""
    fields = []
    for child in root:
        fields.extend(_collect_leaves(child))
    return fields


def _collect_leaves(elem: ET.Element) -> list[str]:
    """Recursively collect leaf element names (no children)."""
    leaves = []
    if len(elem) == 0:
        leaves.append(elem.tag)
    else:
        for child in elem:
            leaves.extend(_collect_leaves(child))
    return leaves


def set_field_values(root: ET.Element, data: dict) -> list[str]:
    """
    Set field values in the XML tree. Handles duplicate field names by setting
    ALL occurrences (single value sets all; list values distribute across matches).

    Returns list of field names that were NOT found.
    """
    missing = []
    for field_name, value in data.items():
        # Find ALL elements with this tag name (handles duplicates like Textfeld1)
        targets = list(root.iter(field_name))

        if targets:
            if isinstance(value, list):
                # Distribute list values across matching elements
                for i, elem in enumerate(targets):
                    if i < len(value):
                        elem.text = str(value[i])
                    else:
                        elem.text = ''
            else:
                # Set all occurrences to the same value
                for elem in targets:
                    elem.text = str(value)
        else:
            missing.append(field_name)

    return missing


def serialize_xml(root: ET.Element, original: str) -> str:
    """Serialize the modified XML tree, preserving the original namespace.

    Uses ET.register_namespace() + ET.indent() for clean output, then
    restores the original xmlns declaration via a targeted root-tag replacement.
    Safe against substring collisions because we match the exact root tag
    boundary (opening angle bracket + tag name).
    """
    # Register the namespace prefix so ET.tostring uses it if needed
    ns_match = re.search(r'(xmlns:(\w+))="([^"]+)"', original)
    if ns_match:
        ET.register_namespace(ns_match.group(2), ns_match.group(3))

    # Pretty-print using ET.indent() (Python 3.9+)
    ET.indent(root, space="  ")

    tree_str = ET.tostring(root, encoding='unicode', xml_declaration=False)

    # Restore the original xmlns declaration on the root element.
    # We match "<root_tag" at the very start (after optional whitespace) to
    # avoid substring collisions with child tags.
    if ns_match:
        root_tag = root.tag
        # Match leading whitespace + opening tag name, insert xmlns after it
        pattern = re.compile(r'^(\s*<' + re.escape(root_tag) + r')')
        repl = r'\1 ' + f'{ns_match.group(1)}="{ns_match.group(3)}"'
        tree_str = pattern.sub(repl, tree_str, count=1)

    return tree_str


# ---------------------------------------------------------------------------
# PDF operations
# ---------------------------------------------------------------------------

def get_xfa_datasets(pdf: pikepdf.Pdf) -> tuple[int, str]:
    """
    Locate the datasets packet in the XFA array.
    Returns (index, xml_string).
    """
    try:
        xfa = pdf.Root.AcroForm.XFA
    except (AttributeError, KeyError):
        sys.exit("Error: PDF has no AcroForm or no XFA data. This may not be an XFA form.")

    # XFA is an array: label, content, label, content, ...
    # We look for the "datasets" label
    datasets_index = None
    for i, item in enumerate(xfa):
        raw = bytes(item)
        label = raw.decode('utf-8', errors='replace').strip()
        if label == 'datasets':
            datasets_index = i + 1  # Content follows the label
            break

    if datasets_index is None or datasets_index >= len(xfa):
        sys.exit("Error: Could not find 'datasets' packet in XFA array.")

    xml_bytes = bytes(xfa[datasets_index])
    xml_str = xml_bytes.decode('utf-8')
    return datasets_index, xml_str


def list_fields(pdf_path: str) -> None:
    """List all data fields in an XFA form."""
    pdf = pikepdf.Pdf.open(pdf_path)
    _, xml_str = get_xfa_datasets(pdf)

    cleaned = strip_namespaces(xml_str)
    root = ET.fromstring(cleaned)

    # Find the top-level form element (child of xfa:data)
    # Structure: datasets > data > Formular1 (or similar) > fields
    data_elem = root.find('data')
    if data_elem is None:
        # Try without the data wrapper
        data_elem = root

    # Get the form element (first child of data, or root itself)
    form_elem = data_elem[0] if data_elem is not None and len(data_elem) > 0 else data_elem

    if form_elem is None:
        sys.exit("Error: Could not find form data element in XFA XML.")

    fields = find_leaf_fields(form_elem)
    if not fields:
        print("(No data fields found)")
        return

    # Deduplicate for counting, but show all occurrences
    unique_fields = sorted(set(fields))
    print(f"Found {len(fields)} field(s) ({len(unique_fields)} unique) in form '{form_elem.tag}':")
    print()

    # Group by name to handle duplicates
    field_counts = collections.Counter(fields)

    for field in fields:
        # Find the FIRST occurrence using iter() for recursive search
        elem = next(form_elem.iter(field), None)
        value = ''
        if elem is not None:
            value = (elem.text or '').strip()
        dup_note = f" [{field_counts[field]} occurrences]" if field_counts[field] > 1 else ""
        print(f"  {field:<45s} = {value!r}{dup_note}")


def fill_form(pdf_path: str, output_path: str, data: dict) -> None:
    """Fill an XFA form with the given data."""
    pdf = pikepdf.Pdf.open(pdf_path)
    datasets_index, original_xml = get_xfa_datasets(pdf)

    cleaned = strip_namespaces(original_xml)
    root = ET.fromstring(cleaned)

    # Navigate to the form element
    data_elem = root.find('data')
    if data_elem is None:
        data_elem = root

    form_elem = data_elem[0] if data_elem is not None and len(data_elem) > 0 else data_elem

    if form_elem is None:
        sys.exit("Error: Could not find form data element in XFA XML.")

    # Set field values
    missing = set_field_values(form_elem, data)

    if missing:
        print(f"Warning: Field(s) not found: {', '.join(missing)}", file=sys.stderr)

    # Serialize back
    modified_xml = serialize_xml(root, original_xml)

    # Write back to PDF — use pikepdf.Stream for proper Stream object
    pdf.Root.AcroForm.XFA[datasets_index] = pikepdf.Stream(
        pdf, data=modified_xml.encode('utf-8')
    )

    pdf.save(output_path)
    print(f"Done. Saved filled form to: {output_path}")

    # Verify: print what was written
    verify_xml = bytes(pdf.Root.AcroForm.XFA[datasets_index]).decode('utf-8')
    verify_cleaned = strip_namespaces(verify_xml)
    verify_root = ET.fromstring(verify_cleaned)
    verify_data = verify_root.find('data')
    if verify_data is None:
        verify_data = verify_root
    verify_form = verify_data[0] if verify_data is not None and len(verify_data) > 0 else verify_data

    print("\nWritten values:")
    for field, value in data.items():
        targets = list(verify_form.iter(field))
        if targets:
            vals = [e.text for e in targets]
            if len(vals) == 1:
                print(f"  ✓ {field} = {vals[0]!r}")
            else:
                print(f"  ✓ {field} = {vals}")
        else:
            print(f"  ✗ {field} = (NOT WRITTEN — field not found)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect and fill XFA (Adobe LiveCycle) PDF forms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # --- fields ---
    fields_parser = subparsers.add_parser('fields', help='List all data fields in the form')
    fields_parser.add_argument('pdf', help='Path to the XFA PDF form')

    # --- fill ---
    fill_parser = subparsers.add_parser('fill', help='Fill the form with data')
    fill_parser.add_argument('pdf', help='Path to the XFA PDF form')
    fill_parser.add_argument('-o', '--output', required=True, help='Output PDF path')
    fill_parser.add_argument('-d', '--data', help='JSON file with field values')
    fill_parser.add_argument('--stdin', action='store_true', help='Read JSON data from stdin')
    fill_parser.add_argument('--set', action='append', dest='sets',
                             help='Set field=value (can be repeated)')

    args = parser.parse_args()

    if args.command == 'fields':
        list_fields(args.pdf)

    elif args.command == 'fill':
        data = {}

        # Load from JSON file
        if args.data:
            with open(args.data, 'r') as f:
                d = json.load(f)
            if not isinstance(d, dict):
                sys.exit("Error: JSON root must be an object (dict)")
            data.update(d)

        # Load from stdin
        if args.stdin:
            d = json.load(sys.stdin)
            if not isinstance(d, dict):
                sys.exit("Error: JSON root must be an object (dict)")
            data.update(d)

        # Parse --set arguments
        if args.sets:
            for item in args.sets:
                if '=' not in item:
                    sys.exit(f"Error: --set requires KEY=VALUE format, got: {item}")
                key, value = item.split('=', 1)
                data[key] = value

        if not data:
            sys.exit("Error: No data provided. Use -d, --stdin, or --set.")

        fill_form(args.pdf, args.output, data)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
