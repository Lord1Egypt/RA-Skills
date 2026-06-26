import lance
import uuid
from datetime import datetime
import pandas as pd
import os
import json
from manage import get_data_path, create_response

def create_dataset(dataset_name, fields):
    try:
        df = pd.DataFrame({
            "_id": [uuid.uuid4().__str__()],
            "dataset_name": [dataset_name],
            "fields": [json.dumps(fields)],
            "_created_at": [datetime.now()]
        })

        metadata_path = os.path.join(get_data_path(), "metadata.lance")
        lance.write_dataset(df, metadata_path, mode="append")

        return create_response("create_dataset", "success", None, None)
    except Exception as e:
        return create_response("create_dataset", "error", None, str(e))

def check_dataset_exists(dataset_name):
    try:
        metadata_path = os.path.join(get_data_path(), "metadata.lance")
        metadata_ds = lance.dataset(metadata_path)
        metadata_df = metadata_ds.to_table().to_pandas()
        matching_rows = metadata_df[metadata_df['dataset_name'] == dataset_name]
        if matching_rows.empty:
            raise ValueError(f"Dataset {dataset_name} does not exist in metadata.")
        fields_data = matching_rows.iloc[0]['fields']
        if isinstance(fields_data, str):
            return json.loads(fields_data)
        else:
            return fields_data
    except Exception as e:
        raise ValueError(f"Error checking dataset metadata: {str(e)}")

def validate_field_count(fields, new_data):
    if len(fields) != len(new_data):
        raise ValueError(f"Number of fields mismatch: expected {len(fields)}, got {len(new_data)}")

def append_to_dataset(new_data, dataset_name):
    try:
        fields = check_dataset_exists(dataset_name)
        validate_field_count(fields, new_data)

        # Create a dictionary with _id, _updated_at, and the field data
        data_dict = {
            "_id": uuid.uuid4().__str__(),
            "_updated_at": datetime.now()
        }
        for field, value in zip(fields, new_data):
            data_dict[field] = value

        df = pd.DataFrame([data_dict])

        dataset_path = os.path.join(get_data_path(), dataset_name)
        lance.write_dataset(df, dataset_path, mode="append")
        return create_response("append_to_dataset", "success", None, None)
    except Exception as e:
        return create_response("append_to_dataset", "error", None, str(e))

def update_dataset_record(dataset_name, record_id, updated_data):
    try:
        fields = check_dataset_exists(dataset_name)
        validate_field_count(fields, updated_data)

        # Load the dataset
        dataset_path = os.path.join(get_data_path(), dataset_name)
        ds = lance.dataset(dataset_path)
        df = ds.to_table().to_pandas()

        # Find the record to update
        record_index = df[df['_id'] == record_id].index
        if len(record_index) == 0:
            raise ValueError(f"Record with ID {record_id} not found in dataset {dataset_name}")

        # Update the record
        for field, value in zip(fields, updated_data):
            df.at[record_index[0], field] = value
        df.at[record_index[0], '_updated_at'] = datetime.now()

        # Write back the updated dataset
        lance.write_dataset(df, dataset_path, mode="overwrite")
        return create_response("update_dataset_record", "success", None, None)
    except Exception as e:
        return create_response("update_dataset_record", "error", None, str(e))

def delete_dataset_record(dataset_name, record_id):
    try:
        check_dataset_exists(dataset_name)

        # Load the dataset
        dataset_path = os.path.join(get_data_path(), dataset_name)
        ds = lance.dataset(dataset_path)
        df = ds.to_table().to_pandas()

        # Find the record to delete
        record_index = df[df['_id'] == record_id].index
        if len(record_index) == 0:
            raise ValueError(f"Record with ID {record_id} not found in dataset {dataset_name}")

        # Remove the record
        df = df.drop(record_index[0])

        # Write back the updated dataset
        lance.write_dataset(df, dataset_path, mode="overwrite")
        return create_response("delete_dataset_record", "success", None, None)
    except Exception as e:
        return create_response("delete_dataset_record", "error", None, str(e))

def batch_append_to_dataset(dataset_name, batch_data):
    try:
        fields = check_dataset_exists(dataset_name)

        # Validate all records in the batch
        for data in batch_data:
            validate_field_count(fields, data)

        # Create DataFrame for batch data
        records = []
        for data in batch_data:
            data_dict = {
                "_id": uuid.uuid4().__str__(),
                "_updated_at": datetime.now()
            }
            for field, value in zip(fields, data):
                data_dict[field] = value
            records.append(data_dict)

        df = pd.DataFrame(records)

        # Append the batch
        dataset_path = os.path.join(get_data_path(), dataset_name)
        lance.write_dataset(df, dataset_path, mode="append")
        return create_response("batch_append_to_dataset", "success", None, None)
    except Exception as e:
        return create_response("batch_append_to_dataset", "error", None, str(e))