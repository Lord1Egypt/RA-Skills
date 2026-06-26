import argparse
import json
from write import *
from manage import *
from read import *

def main():
    parser = argparse.ArgumentParser(description="Lance Dataset Management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # create-dataset
    create_parser = subparsers.add_parser('create-dataset', help='Create a new dataset')
    create_parser.add_argument('dataset_name', help='Name of the dataset')
    create_parser.add_argument('fields', nargs='+', help='List of field names')

    # append-to-dataset
    append_parser = subparsers.add_parser('append-to-dataset', help='Append a record to a dataset')
    append_parser.add_argument('dataset_name', help='Name of the dataset')
    append_parser.add_argument('data', nargs='+', help='Data values for the record')

    # update-dataset-record
    update_parser = subparsers.add_parser('update-dataset-record', help='Update a record in a dataset')
    update_parser.add_argument('dataset_name', help='Name of the dataset')
    update_parser.add_argument('record_id', help='ID of the record to update')
    update_parser.add_argument('data', nargs='+', help='Updated data values')

    # delete-dataset-record
    delete_parser = subparsers.add_parser('delete-dataset-record', help='Delete a record from a dataset')
    delete_parser.add_argument('dataset_name', help='Name of the dataset')
    delete_parser.add_argument('record_id', help='ID of the record to delete')

    # batch-append-to-dataset
    batch_parser = subparsers.add_parser('batch-append-to-dataset', help='Append multiple records to a dataset')
    batch_parser.add_argument('dataset_name', help='Name of the dataset')
    batch_parser.add_argument('batch_data', help='Batch data as JSON string')

    # backup-dataset
    backup_parser = subparsers.add_parser('backup-dataset', help='Backup a dataset')
    backup_parser.add_argument('dataset_name', help='Name of the dataset')
    backup_parser.add_argument('backup_path', help='Path to backup location')

    # list-datasets
    subparsers.add_parser('list-datasets', help='List all datasets')

    # get-dataset-info
    info_parser = subparsers.add_parser('get-dataset-info', help='Get information about a dataset')
    info_parser.add_argument('dataset_name', help='Name of the dataset')

    # list-datasets-info
    subparsers.add_parser('list-datasets-info', help='Get information about all datasets')

    # get-dataset-path-info
    path_parser = subparsers.add_parser('get-dataset-path-info', help='Get path information for a dataset')
    path_parser.add_argument('dataset_name', help='Name of the dataset')

    # drop-dataset
    drop_parser = subparsers.add_parser('drop-dataset', help='Delete a dataset and its metadata entry')
    drop_parser.add_argument('dataset_name', help='Name of the dataset')

    # read-dataset
    read_parser = subparsers.add_parser('read-dataset', help='Read all records from a dataset')
    read_parser.add_argument('dataset_name', help='Name of the dataset')

    # get-record
    record_parser = subparsers.add_parser('get-record', help='Get a specific record by ID')
    record_parser.add_argument('dataset_name', help='Name of the dataset')
    record_parser.add_argument('record_id', help='ID of the record')

    # list-records
    list_parser = subparsers.add_parser('list-records', help='List records from a dataset with pagination')
    list_parser.add_argument('dataset_name', help='Name of the dataset')
    list_parser.add_argument('--limit', type=int, default=100, help='Number of records to return')
    list_parser.add_argument('--offset', type=int, default=0, help='Offset for pagination')

    # count-records
    count_parser = subparsers.add_parser('count-records', help='Count records in a dataset')
    count_parser.add_argument('dataset_name', help='Name of the dataset')

    args = parser.parse_args()

    if args.command == 'create-dataset':
        response = create_dataset(args.dataset_name, args.fields)
    elif args.command == 'append-to-dataset':
        response = append_to_dataset(args.data, args.dataset_name)
    elif args.command == 'update-dataset-record':
        response = update_dataset_record(args.dataset_name, args.record_id, args.data)
    elif args.command == 'delete-dataset-record':
        response = delete_dataset_record(args.dataset_name, args.record_id)
    elif args.command == 'batch-append-to-dataset':
        batch_data = json.loads(args.batch_data)
        response = batch_append_to_dataset(args.dataset_name, batch_data)
    elif args.command == 'backup-dataset':
        response = backup_dataset(args.dataset_name, args.backup_path)
    elif args.command == 'list-datasets':
        response = list_datasets()
    elif args.command == 'get-dataset-info':
        response = get_dataset_info(args.dataset_name)
    elif args.command == 'list-datasets-info':
        response = list_datasets_info()
    elif args.command == 'get-dataset-path-info':
        response = get_dataset_path_info(args.dataset_name)
    elif args.command == 'drop-dataset':
        response = drop_dataset(args.dataset_name)
    elif args.command == 'read-dataset':
        response = read_dataset(args.dataset_name)
    elif args.command == 'get-record':
        response = get_record(args.dataset_name, args.record_id)
    elif args.command == 'list-records':
        response = list_records(args.dataset_name, args.limit, args.offset)
    elif args.command == 'count-records':
        response = count_records(args.dataset_name)
    else:
        response = json.dumps({"skill": "data-vault", "operation": "unknown", "status": "error", "data": None, "error": "Unknown command"})

    print(response)

if __name__ == '__main__':
    main()